"""
~~~~~~~~~~~
Dictalchemy
~~~~~~~~~~~

Contains asdict() and fromdict() methods that will work on SQLAlchemy
declarative models.

Read more in the source or on github
<https://github.com/danielholmstrom/dictalchemy>.
"""

import os
from setuptools import find_packages
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

# Requirements for the package
install_requires = [
    'SQLAlchemy==0.8.0b2',
]

# Requirement for running tests
test_requires = install_requires

setup(name='dictalchemy',
      version='0.1b2',
      description="Contains asdict and fromdict methods for SQL-Alchemy "
      "declarative models",
      long_description=__doc__,
      url='http://github.com/danielholmstrom/dictalchemy/',
      license='MIT',
      author='Daniel Holmstrom',
      author_email='holmstrom.daniel@gmail.com',
      platforms='any',
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   'Topic :: Software Development :: '
                   'Libraries :: Python Modules'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=test_requires,
      test_suite='dictalchemy',
      )
