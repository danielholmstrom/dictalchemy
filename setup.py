"""
Setup the package

`include_package_data' will add all files in MANIFEST.in that is prefixed
'recursive-include'.

"""
import os
from setuptools import find_packages
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

# Requirements for the package
install_requires = ['Sphinx==1.1.3',
        'nose==1.2.1',
        'coverage==3.5.2',
        'SQLAlchemy==0.8.0b2',
        ]


# Requirement for running tests
test_requires = install_requires

setup(name='Iteralchemy',
    version='0.1',
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=test_requires,
    test_suite='iteralchemy',
    )
