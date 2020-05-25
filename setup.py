# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Main Package Manager.
Author: Dodo325
GitLab: https://github.com/dodo325/
"""
from glob import glob
from setuptools import setup, find_packages
import sys
import mpm
import os

def get_all_files(base_dir: str) -> list:
    files = []
    for r, d, f in os.walk(base_dir):
        for file in f:
            files.append(os.path.join(r, file))
    return files

REQUIREMENTS = [
    "click>=7.0"
]


def main():
    setup(name='mpm',
          version=mpm.__version__,
          description=sys.modules[__name__].__doc__,
          long_description=open('README.md').read(),
          long_description_content_type='text/markdown',
          author='Dodo325',
          url='https://github.com/dodo325/mpm',
          #   download_url='github.com/...',
          license='GNU GPL',
          python_requires='>=3.7, <4',
          install_requires=REQUIREMENTS,
          extras_require={
              'test': ['pytest']
          },
          classifiers=[
              "Environment :: Console",
              "Intended Audience :: Developers",
              'Programming Language :: Python :: 3.7',
              'Programming Language :: Python :: 3.8',
              "Programming Language :: Python :: 3 :: Only",
              'Topic :: Software Development :: Libraries',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Utilities'
          ],
          keywords=[
              "package-manager"
          ],
          packages=find_packages(include=['mpm']),
          entry_points={
              'console_scripts':
              ['mpm = mpm.core.cli:main']
          },
          include_package_data=True,
          data_files=[
                ('configs', get_all_files("configs/")),
                ('kits', get_all_files("kits/")),
                ('configs', get_all_files("scripts/")),
              ],
        #   project_urls={  # Optional
        #       'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        #       'Funding': 'https://donate.pypi.org',
        #       'Say Thanks!': 'http://saythanks.io/to/example',
        #       'Source': 'https://github.com/pypa/sampleproject/',
        #   },
    )

if __name__ == '__main__':
    main()
