#!/usr/bin/env python

"""Setuptools params"""

from setuptools import setup, find_packages
from os.path import join

# Get version number from source tree
import sys
sys.path.append('.')
from heatgen import VERSION

scripts = [join('bin', filename) for filename in ['heatgen']]
modname = distname = 'heatgen'

setup(
    name=distname,
    version=VERSION,
    description='A tool to generate heat template in JSON format',
    author='Baohua Yang',
    author_email='yangbaohua@gmail.com',
    #packages=['heatgen'],
    packages=find_packages(),
    long_description="""
        More details please go to
        https://github.com/yeasy/heatgen
        """,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        ],
    keywords='Cloud OpenStack Heat',
    license='BSD',
    install_requires=[
        'setuptools>=1.0',
        'oslo.config>=1.2',
        'python-novaclient>=2.0',
        'python-neutronclient>=2.0',
        'python-keystoneclient>=0.9',
    ],
    scripts=scripts,
)
