from setuptools import setup, find_packages
import os

# Read the README file for the long description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='function_notifier', 
    version='1.0.1',           
    author='Lewis Dean',
    description='This package contains the notify decorator, used to '
                'notify users when the wrapped function has finished '
                'execution.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/LewisDean22/function_notifier",
    packages=find_packages(),  # Automatically find all packages and subpackages
    classifiers=[                
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[  
        'plyer>=2.1.0',  
    ],
)
