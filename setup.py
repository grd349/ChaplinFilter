#!/usr/bin/env python3

import os
import sys
from setuptools import setup

# Prepare and send a new release to PyPI
if "release" in sys.argv[-1]:
    os.system("python3 setup.py sdist")
    os.system("python3 -m twine upload dist/* --verbose")
    os.system("rm -rf dist/*")
    sys.exit()

# Load the __version__ variable without importing the package already
exec(open('chaplinfilter/version.py').read())

setup(name='chaplinfilter',
      version=__version__,
      description="A simple package to calculate the filter timescale from"
                  "Chaplin et al. in prep.",
      long_description=open('README.md').read(),
      author='Guy R. Davies',
      author_email='grd349@gmail.com',
      licence='MIT',
      packages=['chaplinfilter'],
      #url='TODO',
      install_requires=['numpy', 'scikit-learn', 'pandas'],
      include_package_data=True,
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering :: Astronomy",
          ],
      )
