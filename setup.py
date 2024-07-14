# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'tenneteu', 'tenneteu.py'), encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        if l.startswith('__version__'):
            __version__ = l.split('"')[1]

setup(
    name='tenneteu-py',
    version=__version__,
    description='A python API wrapper for tennet.eu API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fboerman/TenneTeu-py',
    author='Frank Boerman',
    author_email='frank@fboerman.nl',
    license='MIT',


    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],

    keywords='TenneT data api energy',

    packages=find_packages(),

    install_requires=['requests', 'pandas'],

    include_package_data=True,
)
