# setup.py

from setuptools import setup, find_packages

setup(
    name='OptiVisionNet',
    version='0.1.0',
    description='A package for CNN + BiLSTM + MLP model with GWO optimization for image classification',
    author='Said Al Afghani Edsa',
    author_email= ['saidalafghani.dumai@gmail.com', 'edsa09lab@gmail.com'],
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
