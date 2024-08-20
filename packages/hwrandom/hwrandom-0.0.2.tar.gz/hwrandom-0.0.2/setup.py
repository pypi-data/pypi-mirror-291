from setuptools import setup, find_packages
import codecs
import os

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


VERSION = '0.0.2'
DESCRIPTION = 'The hwrandom Python package uses Intel’s RDRAND instruction to generate high-entropy, cryptographically secure random numbers for various applications.'
LONG_DESCRIPTION = "The hwrandom Python package provides a high-performance random number generator utilizing Intel's RDRAND instruction, a hardware-based source of cryptographically secure random numbers. By interfacing directly with the RDRAND instruction through a shared library, hwrandom delivers true hardware-based randomness, ensuring a higher level of entropy compared to traditional software-based generators. This package offers a variety of functions for generating random integers, floating-point numbers, and selections from sequences, making it a robust tool for applications requiring high-quality randomness and cryptographic security."

# Setting up
setup(
    name="hwrandom",
    version=VERSION,
    author="RaymonDev",
    author_email="ramongallinadcorti@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['random', 'hardware random', 'RDRAND', 'cryptographic randomness', 'random number generator', 'secure random', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)