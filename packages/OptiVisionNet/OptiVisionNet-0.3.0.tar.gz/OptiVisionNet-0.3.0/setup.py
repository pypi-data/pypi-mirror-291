from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='OptiVisionNet',
    version='0.3.0',
    description='Usage example: from OptiVisionNet.model import CNN_BiLSTM_MLP',
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    author='Said Al Afghani Edsa',
    author_email='saidalafghani.dumai@gmail.com',  
    packages=find_packages(),
    install_requires=[
        'torch',
        'numpy',
        'scikit-learn',
        'tqdm',
        'Pillow'
    ],
    python_requires='>=3.6',
)
