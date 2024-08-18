# setup.py

from setuptools import setup, find_packages

setup(
    name="tinkercss",
    version="0.2.0",  # Atjauniniet versijas numuru
    description="A CSS-like styling tool for Tkinter applications",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
