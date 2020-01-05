# -*- coding: utf-8 -*-

"""
Setup file for pharm-drone, using setuptools
"""

from setuptools import setup, find_packages

setup(
    name='pharm-drone',
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'opencv-contrib-python',
        'numpy',
        'sklearn',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        pharm-drone=src.entry:cli
    ''',
)
