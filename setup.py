#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
    long_description = readme.read()

name = 'scrunch'
description = 'Pythonic scripting library for cleaning data in Crunch'
nspkg_technique = 'native'
"""
Does this package use "native" namespace packages or
pkg_resources "managed" namespace packages?
"""

params = dict(
    name=name,
    use_scm_version=True,
    author="Crunch.io",
    author_email="dev@crunch.io",
    description=description or name,
    long_description=long_description,
    url="https://github.com/Crunch-io/" + name,
    packages=setuptools.find_packages(),
    include_package_data=True,
    namespace_packages=(
        name.split('.')[:-1] if nspkg_technique == 'managed'
        else []
    ),
    python_requires='>=2.7',
    install_requires=[
        'pandas<0.20',
        'pycrunch>=0.4.0',
        'requests',
        'six',
    ],
    extras_require={
        'testing': [
            'pytest>=2.8',
            'pytest-sugar',
            'collective.checkdocs',
            'pytest-cov',
            'mock',
            'isodate',
            'backports.unittest_mock',
        ],
        'docs': [
            'sphinx',
            'jaraco.packaging>=3.2',
            'rst.linker>=1.9',
        ],
        'pandas': ['pandas'],
    },
    setup_requires=[
        'setuptools_scm>=1.15.0',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
    },
)
if __name__ == '__main__':
    setuptools.setup(**params)
