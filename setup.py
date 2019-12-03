#!/usr/bin/env python3

import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='fqstat',
    version='1.0.0',
    author='Stephen Lorenz',
    author_email='lorenzsj@clarkson.edu',
    description='Recursively find FastQ files and report the percent of records with nucleotides greater than a provided value per file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lorenzsj/fqstat',
    entry_points={
        'console_scripts': [
            'fqstat = fqstat.fqstat:cli',
        ]
    },
    install_requires=[
        'biopython',
        'prettytable',
    ],
)