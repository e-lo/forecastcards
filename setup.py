#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import io
import os
import sys

from setuptools import setup, find_packages

with open('README.md') as rmfile:
    readme = rmfile.read()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

example_files = package_files('forecastcards/examples')
nb_files      = package_files('forecastcards/notebooks')

print("EXAMPLE FILES",example_files)

requirements = [
    'pandas==0.22',
    'requests',
    'goodtables',
    'tableschema',
    'graphviz',
    'statsmodels',
    'jupyter'
]

test_requirements = [
    'pytest',
]

setup(
    name='forecastcards',
    version='0.1.0dev',
    packages=find_packages(include=['forecastcards']),
    long_description=readme,
    author="Elizabeth Sall",
    author_email='easall@gmail.com',
    url='https://github.com/e-lo/forecastcards',
    include_package_data=True,
    install_requires=requirements,
    package_data={'forecastcards': example_files+nb_files},
    tests_suite = 'tests',
    scripts=['forecastcards/scripts/validate_cardset.py','forecastcards/scripts/validate_project.py'],
    tests_require=test_requirements,
    extra_compile_args = ['-std=c++11'],
)
