#!/usr/bin/env python

"""The setup script."""
import os
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    with open(os.path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


requirements = []

test_requirements = []

setup(
    author="Han Zhichao",
    author_email='superhin@126.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="unittest enhancement",
    entry_points={
        'console_scripts': [
            'unitplus=unitplus.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    # long_description=readme + '\n\n' + history,
    # long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='unitplus',
    name='unitplus',
    packages=find_packages(include=['unitplus', 'unitplus.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hanzhichao/unitplus',
    version='0.1.2',
    zip_safe=False,
)
