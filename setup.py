from os import chdir
from os.path import abspath, dirname, join, normpath
from setuptools import find_packages, setup


def read_file(filename):
    with open(join(dirname(abspath(__file__)), filename)) as f:
        return f.read()


# allow setup.py to be run from any path
chdir(normpath(abspath(dirname(__file__))))

import behave_django  # noqa

setup(
    name='behave-django',
    version=behave_django.__version__,
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    license=behave_django.__license__,
    description=behave_django.__doc__.strip(),
    long_description=read_file('README.rst'),
    url='https://github.com/behave/behave-django',
    author='Mitchel Cabuloy',
    author_email='mixxorz@gmail.com',
    maintainer='Mitchel Cabuloy, Peter Bittner',
    maintainer_email='mixxorz@gmail.com',
    install_requires=read_file('requirements.txt'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Testing',
    ],
    test_suite='tests',
)
