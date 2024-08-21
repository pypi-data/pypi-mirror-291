# setup.py

from setuptools import setup, find_packages

setup(
    name="genetic_algorithms_personal",
    version="0.1.0",
    author="NinjaNick",
    author_email="nicholas.starbuck@mnstu.catholic.edu.au",
    description="A custom genetic algorithm package with Pygame visualization.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pygame",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
