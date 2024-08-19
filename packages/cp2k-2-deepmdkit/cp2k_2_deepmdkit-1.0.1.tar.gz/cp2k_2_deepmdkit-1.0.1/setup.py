from setuptools import setup, find_packages
from pathlib import Path

# Define the long description
this_directory = Path(__file__).parent
long_description = """
cp2k-2-deepmdkit (c2d): A comprehensive tool for converting cp2k output to DeepMD-kit input.

This package includes a set of utilities for processing CP2K output files into a format compatible with DeepMD-kit. It provides several command-line tools for coordinate extraction, force and energy data processing, box dimensions extraction, and file format conversion.
"""

setup(
    name='cp2k_2_deepmdkit',
    version='1.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'c2d-coord=cp2k_to_deepmdkit.coord:main',
            'c2d-force_energy=cp2k_to_deepmdkit.force_energy:main',
            'c2d-box=cp2k_to_deepmdkit.box:main',
            'c2d-convert=cp2k_to_deepmdkit.convert:main',
        ],
    },
    install_requires=[],
    long_description=long_description,  # Updated long description
    long_description_content_type='text/markdown',  # Specify the format (if markdown, otherwise use text/x-rst for reStructuredText)
)
