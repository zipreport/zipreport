#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# Check python version
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("Unsupported Python version - Python {}.{} or greater required.".format(*REQUIRED_PYTHON))
    sys.exit(1)

version = __import__('zipreport').get_version()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

# read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    description = f.read()

setup(
    name='zipreport-lib',
    version=version,
    author="Joao Pinheiro",
    author_email="",
    url="https://github.com/zipreport/zipreport",
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    description='Python HTML reporting engine',
    license='MIT',
    long_description=description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Printing',
    ],
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jinja2>=2.11",
        "requests"
    ],
    zip_safe=False,
    tests_require=[
        "jinja2>=2.11",
        "requests",
        "coverage==4.4.1",
        "mock>=1.0.1",
        "flake8>=2.1.0",
        "tox>=1.7.0",
        "codecov>=2.0.0",
        "pytest-cov>=2.8.1",
    ],
    entry_points={
        'console_scripts': [
            'zipreport=zipreport.cli.console:main',
        ],
    }
)
