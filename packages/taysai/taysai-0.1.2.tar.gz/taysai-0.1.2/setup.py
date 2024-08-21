# setup.py

from setuptools import setup, find_packages

setup(
    name='taysai',
    version='0.1.2',
    description='A utility package for saving PyTorch models with automatic import detection.',
    author='Taylor',
    author_email='your-email@example.com',  # Replace with your email
    url='https://github.com/yourusername/taysai',  # Replace with your GitHub URL
    packages=find_packages(),
    install_requires=[
        'torch',
        'dill'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
