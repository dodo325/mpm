#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main Package Manager.
Author: Dodo325
GitHub: https://github.com/dodo325/
"""
from setuptools import setup, find_packages
import sys
import mpm
import os
from rich.console import Console

REQUIREMENTS = [
    "plumbum",
    "rich"
]


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        console.print_exception()
        return ""

setup_config = {
    "name": "mpm-core",
    "version": mpm.__version__,
    "description": sys.modules[__name__].__doc__,
    # long_description=read("README"),
    "author": "Dodo325",
    "url": "https://github.com/dodo325/mpm",
    "license": "GPLv3",
    "python_requires": ">=3.7, <4",
    "install_requires": REQUIREMENTS,
    "extras_require": {
        "test": [
            "pytest", 
            "pytest-subprocess",
            "pytest-cov",
            "coloredlogs",
            "codecov"
        ],
        "docs": [
            "markdown-fenced-code-tabs"
        ]
    },
    "classifiers": [
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    "keywords": ["package-manager"],
    "packages": find_packages(exclude=["tests"]),
    "entry_points": {"console_scripts": ["mpm=mpm.core.cli:main"]},
    "include_package_data": True,
    #   project_urls={  # Optional
    #       'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
    #       'Funding': 'https://donate.pypi.org',
    #       'Say Thanks!': 'http://saythanks.io/to/example',
    #       'Source': 'https://github.com/pypa/sampleproject/',
    #   },
}

def main():
    setup(**setup_config)

if __name__ == "__main__":
    main()
