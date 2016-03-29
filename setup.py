#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="Matlabette",
    version="0.1",
    packages=find_packages(),
    author="Humphrey Thuo",
    author_email="thuohm@gmail.com",
    description="A minimal REPL clone of MATLAB",
    long_description="""
Matlabette
=========

Matlabette is a minimal REPL clone of MATLAB.

Features
--------
 * Array creation

 * Array and matrix operations

 * Array concatenation

 * Saving and loading workspace

""",
    license="MIT",
    keywords="matlab repl matlabette mini minimal",
    url="https://github.com/thuo/bc-6-matlabette",
)
