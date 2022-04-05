#!/usr/bin/env python3
"""
Packaging setup of Django integration for behave.
"""
from pathlib import Path

from setuptools import find_packages, setup

import behave_django as package


def read_file(filename):
    """Read a text file and return its contents."""
    project_home = Path(__file__).parent.resolve()
    file_path = project_home / filename
    return file_path.read_text(encoding="utf-8")


setup(
    name='behave-django',
    version=package.__version__,
    description=package.__doc__.strip(),
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    url='https://github.com/behave/behave-django',
    project_urls={
        'Documentation': 'https://behave-django.readthedocs.io/',
    },
    author='Mitchel Cabuloy',
    author_email='mixxorz@gmail.com',
    maintainer='Peter Bittner, Javier Buzzi',
    maintainer_email='django+SPAM@bittner.it',
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    install_requires=read_file('requirements.txt'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Testing',
    ],
    test_suite='tests',
)
