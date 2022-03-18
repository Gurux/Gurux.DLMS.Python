#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='GuruxDlmsSample',
    description='Client for DLMS protocol',
    version='0.1.0',
    author='maekos',
    author_email='maekos@gmail.com',
    url='https://github.com/Gurux/Gurux.DLMS.Python',
    scripts=['bin/GuruxDlmsSample'],
    packages=[
        '.'
    ],
    install_requires=[
        'gurux-common',
        'gurux-dlms',
        'gurux-net',
        'gurux-serial',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7.4",
    ],
)
