#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='dictlist',
    packages=['dictlist'],
    version='0.0.1',
    description='Search list of dictionaries',
    author='Solomon Huang',
    author_email='huang.solomon@gmail.com',
    url='https://github.com/solhuang/dictlist',
    license='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
