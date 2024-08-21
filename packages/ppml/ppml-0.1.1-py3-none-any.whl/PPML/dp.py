import argparse
import os
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data
import torch.utils.data.dataloader
import torchvision.datasets as dset
import torchvision.transforms as transforms
import warnings
from opacus.validators import ModuleValidator
from opacus import PrivacyEngine

# Set CUBLAS workspace configuration
os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'

# Suppress warnings
warnings.simplefilter("ignore")

def initialize_weights(module):
    """
    Initialize weights for the model as suggested in https://arxiv.org/abs/1511.06434.

    Args:
        module (nn.Module): The module to initialize weights for.
    """
    class_name = module.__class__.__name__
    if class_name.find('Conv') != -1:
        nn.init.normal_(module.weight.data, 0.0, 0.02)
    elif class_name.find('BatchNorm') != -1:
        nn.init.normal_(module.weight.data, 1.0, 0.02)
        nn.init.constant_(module.bias.data, 0)

class Generator(nn.Module):
    """Generator network for the GAN."""

    def __init__(self, num_gpus, latent_vector_size, generator_feature_map_size, num_channels):
        """
        Initialize the Generator.

        Args:
            num_gpus (int): Number of GPUs available.
            latent_vector_size (int): Size of the latent vector.
            generator_feature_map_size (int): Size of feature maps in generator.
            num_channels (int): Number of channels in the output image.
        """
        super(Generator, self).__init__()
        self.num_gpus = num_gpus
        self.main = nn.Sequential(
            # Initial transposed convolution
            nn.ConvTranspose2d(latent_vector_size, generator_feature_map_size * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(generator_feature_map_size * 8),
            nn.ReLU(True),
            
            # Series of transposed convolutions
            nn.ConvTranspose2d(generator_feature_map_size * 8, generator_feature_map_size * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(generator_feature_map_size * 4),
            nn.ReLU(True),
            
            nn.ConvTranspose2d(generator_feature_map_size * 4, generator_feature_map_size * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(generator_feature_map_size * 2),
            nn.ReLU(True),
            
            nn.ConvTranspose2d(generator_feature_map_size * 2, generator_feature_map_size, 4, 2, 1, bias=False),
            nn.BatchNorm2d(generator_feature_map_size),
            nn.ReLU(True),
            
            # Output layer
            nn.ConvTranspose2d(generator_feature_map_size, num_channels, 4, 2, 1, bias=False),
            nn.Tanh()
        )
    
    def forward(self, input_tensor):
        """
        Forward pass of the generator.

        Args:
            input_tensor (torch.Tensor): Input tensor (latent vector).

        Returns:
            torch.Tensor: Generated image.
        """
        return self.main(input_tensor)


class Discriminator(nn.Module):
    """Discriminator network for the GAN."""

    def __init__(self, num_gpus, discriminator_feature_map_size, num_channels):
        """
        Initialize the Discriminator.

        Args:
            num_gpus (int): Number of GPUs available.
            discriminator_feature_map_size (int): Size of feature maps in discriminator.
            num_channels (int): Number of channels in the input image.
        """
        super(Discriminator, self).__init__()
        self.num_gpus = num_gpus
        self.main = nn.Sequential(
            # Initial convolution
            nn.Conv2d(num_channels, discriminator_feature_map_size, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            
            # Series of convolutions
            nn.Conv2d(discriminator_feature_map_size, discriminator_feature_map_size * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(discriminator_feature_map_size * 2),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Conv2d(discriminator_feature_map_size * 2, discriminator_feature_map_size * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(discriminator_feature_map_size * 4),
            nn.LeakyReLU(0.2, inplace=True),
            
            nn.Conv2d(discriminator_feature_map_size * 4, discriminator_feature_map_size * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(discriminator_feature_map_size * 8),
            nn.LeakyReLU(0.2, inplace=True),
            
            # Output layer
            nn.Conv2d(discriminator_feature_map_size * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )
    
    def forward(self, input_tensor):
        """
        Forward pass of the discriminator.

        Args:
            input_tensor (torch.Tensor): Input tensor (image).

        Returns:
            torch.Tensor: Probability of input being real.
        """
        return self.main(input_tensor)

def main():
    # Hyperparameters and constants
    MAX_GRADIENT_NORM = 4.0
    PRIVACY_EPSILON = 50.0
    PRIVACY_DELTA = 1e-5
    dataset_root = "data/celeba"
    num_workers = 2
    batch_size = 128
    image_size = 64
    num_channels = 3
    latent_vector_size = 100
    generator_feature_map_size = 64
    discriminator_feature_map_size = 64
    num_epochs = 5
    learning_rate = 0.0002
    beta1 = 0.5
    num_gpus = 1

    # Set device
    device = set_device()
    print("Device =", device)

    # Load and preprocess dataset
    dataset, dataloader = load_and_preprocess_data(dataset_root, image_size, batch_size, num_workers)
    print("Size of dataset:", len(dataset))

    # Initialize Generator and Discriminator
    generator = initialize_generator(num_gpus, latent_vector_size, generator_feature_map_size, num_channels, device)
    discriminator = initialize_discriminator(num_gpus, discriminator_feature_map_size, num_channels, device)

    # Validate model for privacy
    discriminator = ModuleValidator.fix(discriminator)

    # Loss function and optimizers
    criterion = nn.BCELoss()
    discriminator_optimizer = optim.Adam(discriminator.parameters(), lr=learning_rate, betas=(beta1, 0.999))
    generator_optimizer = optim.Adam(generator.parameters(), lr=learning_rate, betas=(beta1, 0.999))

    # Initialize privacy engine
    print("Initializing privacy engine...")
    privacy_engine, (discriminator, discriminator_optimizer, dataloader) = initialize_privacy_engine(discriminator, discriminator_optimizer, dataloader, num_epochs, PRIVACY_EPSILON, PRIVACY_DELTA, MAX_GRADIENT_NORM)

    # Training loop
    print("Starting Training Loop...")
    for epoch in range(num_epochs):
        train_epoch(discriminator, generator, dataloader, discriminator_optimizer, generator_optimizer, criterion, device, latent_vector_size, epoch, num_epochs, PRIVACY_DELTA, privacy_engine)

def set_device():
    """
    Set the device for PyTorch computations.

    Returns:
        torch.device: The selected device (CUDA, MPS, or CPU).
    """
    return torch.device("cuda" if torch.cuda.is_available() else 
                        "mps" if torch.backends.mps.is_available() else 
                        "cpu")

def load_and_preprocess_data(dataset_root, image_size, batch_size, num_workers):
    """
    Load and preprocess the dataset.

    Args:
        dataset_root (str): Root directory of the dataset.
        image_size (int): Size to which images should be resized.
        batch_size (int): Number of samples per batch.
        num_workers (int): Number of subprocesses to use for data loading.

    Returns:
        tuple: A tuple containing the dataset and dataloader.
    """
    transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))
    ])
    dataset = dset.ImageFolder(root=dataset_root, transform=transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    return dataset, dataloader

def initialize_generator(num_gpus, latent_vector_size, generator_feature_map_size, num_channels, device):
    """
    Initialize the Generator network.

    Args:
        num_gpus (int): Number of GPUs available.
        latent_vector_size (int): Size of the latent vector.
        generator_feature_map_size (int): Size of feature maps in generator.
        num_channels (int): Number of channels in the output image.
        device (torch.device): Device to which the model should be moved.

    Returns:
        nn.Module: Initialized Generator model.
    """
    generator = Generator(num_gpus, latent_vector_size, generator_feature_map_size, num_channels).to(device)
    if (device.type == 'cuda' or device.type == 'mps') and num_gpus > 1:
        generator = nn.DataParallel(generator, list(range(num_gpus)))
    generator.apply(initialize_weights)
    return generator

def initialize_discriminator(num_gpus, discriminator_feature_map_size, num_channels, device):
    """
    Initialize the Discriminator network.

    Args:
        num_gpus (int): Number of GPUs available.
        discriminator_feature_map_size (int): Size of feature maps in discriminator.
        num_channels (int): Number of channels in the input image.
        device (torch.device): Device to which the model should be moved.

    Returns:
        nn.Module: Initialized Discriminator model.
    """
    discriminator = Discriminator(num_gpus, discriminator_feature_map_size, num_channels).to(device)
    if (device.type == 'cuda' or device.type == 'mps') and num_gpus > 1:
        discriminator = nn.DataParallel(discriminator, list(range(num_gpus)))
    discriminator.apply(initialize_weights)
    return discriminator

def initialize_privacy_engine(discriminator, discriminator_optimizer, dataloader, num_epochs, privacy_epsilon, privacy_delta, max_gradient_norm):
    """
    Initialize the privacy engine for differential privacy.

    Args:
        discriminator (nn.Module): The Discriminator network.
        discriminator_optimizer (torch.optim.Optimizer): Optimizer for the Discriminator.
        dataloader (torch.utils.data.DataLoader): DataLoader for the dataset.
        num_epochs (int): Number of training epochs.
        privacy_epsilon (float): Privacy budget epsilon.
        privacy_delta (float): Privacy parameter delta.
        max_gradient_norm (float): Maximum L2 norm of per-sample gradients.

    Returns:
        tuple: A tuple containing the private model, optimizer, and data loader.
    """
    privacy_engine = PrivacyEngine()
    return privacy_engine, privacy_engine.make_private_with_epsilon(
        module=discriminator,
        optimizer=discriminator_optimizer,
        data_loader=dataloader,
        epochs=num_epochs,
        target_epsilon=privacy_epsilon,
        target_delta=privacy_delta,
        max_grad_norm=max_gradient_norm,
    )

def train_epoch(discriminator, generator, dataloader, discriminator_optimizer, generator_optimizer, criterion, device, latent_vector_size, epoch, num_epochs, privacy_delta, privacy_engine):
    """
    Train the GAN for one epoch.

    Args:
        discriminator (nn.Module): The Discriminator network.
        generator (nn.Module): The Generator network.
        dataloader (torch.utils.data.DataLoader): DataLoader for the dataset.
        discriminator_optimizer (torch.optim.Optimizer): Optimizer for the Discriminator.
        generator_optimizer (torch.optim.Optimizer): Optimizer for the Generator.
        criterion (nn.Module): Loss function.
        device (torch.device): Device on which to perform computations.
        latent_vector_size (int): Size of the latent vector.
        epoch (int): Current epoch number.
        num_epochs (int): Total number of epochs.
        privacy_delta (float): Privacy parameter delta.
        privacy_engine (PrivacyEngine): Privacy engine instance.
    """
    for batch_index, data in enumerate(dataloader, 0):
        discriminator_optimizer.zero_grad()

        # Loss of discriminator with real batch
        real_data = data[0].to(device)
        b_size = real_data.size(0)
        rlabel = torch.full((b_size,), 1, dtype=torch.float, device=device)
        output = discriminator(real_data).view(-1)
        errD_real = criterion(output, rlabel)
        D_x = output.mean().item()

        # Loss of discriminator with fake batch
        noise = torch.randn(b_size, latent_vector_size, 1, 1, device=device)
        fake = generator(noise)
        flabel = torch.full((b_size,), 0, dtype=torch.float, device=device)
        output = discriminator(fake.detach()).view(-1)
        errD_fake = criterion(output, flabel)
        D_G_z1 = output.mean().item()
        errD = errD_real + errD_fake

        # Update discriminator
        errD.backward()
        discriminator_optimizer.step()
        discriminator_optimizer.zero_grad()

        # Loss of generator
        generator_optimizer.zero_grad()
        output = discriminator(fake).view(-1)
        errG = criterion(output, rlabel)
        D_G_z2 = output.mean().item()

        # Update generator
        errG.backward()
        generator_optimizer.step()

        # Print training stats
        if batch_index % 2 == 0:
            print_training_stats(epoch, num_epochs, batch_index, len(dataloader), errD, errG, D_x, D_G_z1, D_G_z2, privacy_delta, privacy_engine)
            save_generator_model(generator)

def print_training_stats(epoch, num_epochs, i, dataloader_len, errD, errG, D_x, D_G_z1, D_G_z2, DELTA, privacy_engine):
    """
    Print training statistics.

    Args:
        epoch (int): Current epoch number.
        num_epochs (int): Total number of epochs.
        i (int): Current batch index.
        dataloader_len (int): Total number of batches.
        errD (float): Discriminator loss.
        errG (float): Generator loss.
        D_x (float): D(x) - Discriminator output for real data.
        D_G_z1 (float): D(G(z)) - Discriminator output for fake data (before Generator update).
        D_G_z2 (float): D(G(z)) - Discriminator output for fake data (after Generator update).
        DELTA (float): Privacy parameter delta.
        privacy_engine (PrivacyEngine): Privacy engine instance.
    """
    print(f'[{epoch}/{num_epochs}][{i}/{dataloader_len}]\t'
          f'Loss_D: {errD.item():.4f}\tLoss_G: {errG.item():.4f}\t'
          f'D(x): {D_x:.4f}\tD(G(z)): {D_G_z1:.4f} / {D_G_z2:.4f}\t'
          f'(ε = {privacy_engine.get_epsilon(DELTA):.4f}, δ = {DELTA:.0e})')

def save_generator_model(netG):
    """
    Save the Generator model state.

    Args:
        netG (nn.Module): The Generator network to be saved.
    """
    torch.save(netG.state_dict(), "netG_dpgan.pth")
    print("Saved Generator Model State to netG_dpgan.pth")

if __name__ == "__main__":
    main()
