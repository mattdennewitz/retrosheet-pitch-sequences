#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name = 'retrosheet-pitch-sequences',
    version = '1.0.1',
    description = 'Retrosheet at-bat ball/strike count state extraction',
    author = 'Matt Dennewitz',
    author_email = 'mattdennewitz@gmail.com',
    url = 'https://github.com/mattdennewitz/retrosheet-pitch-sequences',
    install_requires = ['click==0.6', 'prettytable==0.7.2'],
    py_modules=['rs_pitch_seq'],
    entry_points = {
        'console_scripts': [
            'rs-pitch-seq = rs_pitch_seq:extract_sequences',
        ]
    }
)
