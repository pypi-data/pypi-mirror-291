from setuptools import setup, find_packages

setup(
    name="tinkercss",
    version="0.1.0",
    description="A Python library for generating CSS in a Tinker-like style.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Jūsu Vārds",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/tinkercss",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
