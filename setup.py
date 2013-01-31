"""
~~~~~~~~~~~
Dictalchemy
~~~~~~~~~~~

Contains asdict() and fromdict() methods that will work on SQLAlchemy declarative models.

Read more in the source or on github <https://github.com/danielholmstrom/dictalchemy>.
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

setup(name='dictalchemy',
    version='0.1a3',
    description="Contains asdict and fromdict methods for SQL-Alchemy "
            "declarative models",
    long_description=__doc__,
    url='http://github.com/danielholmstrom/dictalchemy/',
    license='MIT',
    author='Daniel Holmstrom',
    author_email='holmstrom.daniel@gmail.com',
    platforms='any',
    classifiers=['Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=test_requires,
    test_suite='dictalchemy',
    )
