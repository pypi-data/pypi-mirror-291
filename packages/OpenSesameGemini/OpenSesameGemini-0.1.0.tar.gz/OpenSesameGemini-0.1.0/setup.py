# setup.py

from setuptools import setup, find_packages

setup(
    name="OpenSesameGemini",  # Updated package name
    version="0.1.0",
    description="A package to interface with OpenSesame for generative AI models.",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",  # Replace with the correct package name if different
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
