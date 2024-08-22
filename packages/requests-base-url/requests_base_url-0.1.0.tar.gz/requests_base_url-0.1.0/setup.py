#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
import os
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
setup_requirements = []


def read_file(filename):
    with open(os.path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setup(
    author="Han Zhichao",
    author_email='superhin@126.com',
    description='Http client with base_url base on requests',
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",  # 新参数
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    license="MIT license",
    include_package_data=True,
    keywords=[
        'base_url', 'requests', 'http client',
    ],
    name='requests-base-url',
    packages=find_packages(include=['requests_base_url']),
    setup_requires=setup_requirements,
    url='https://github.com/hanzhichao/requests-base-url',
    version='0.1.0',
    zip_safe=True,
    install_requires=['requests']
)
