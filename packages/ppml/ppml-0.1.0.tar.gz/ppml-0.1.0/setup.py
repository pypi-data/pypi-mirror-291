from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ppml",
    version="0.1.0",
    author="Bidhan Roy",
    author_email="bidhan@bagel.net",
    description="A privacy-preserving machine learning package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BagelNetwork/ppml",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "torch>=1.8.0",
        "torchvision>=0.9.0",
        "opacus>=1.0.0",
        "numpy",
        "Pillow",
        "tqdm",
    ],
)
