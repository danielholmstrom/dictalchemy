# vim: set fileencoding=utf-8 :
"""

~~~~~~~~~~~~
Introduction
~~~~~~~~~~~~

This library adds basic functionality for getting a dict from an SQLAlchemy
model and updating a model from a dict.

SQLAlchemy is a very complex library. It contains synonyms, lists, sets, mixins
and god knows what. Automatically convert that to a dict resp. update from a
dict is not a simple task. This library should not be used on more complex
models without thorough testing, it should however be fine to use on simple
models.

~~~~~~~~~~~~~~~~~~~~~
A note about synonyms
~~~~~~~~~~~~~~~~~~~~~

Synonyms wraps a reader and a writer method. These methods can do whatever they
want to so there is no way to safely updated data with synonyms.

~~~~~~~~~~~~~~~~~~~~~~~~~
Bugs and missing features
~~~~~~~~~~~~~~~~~~~~~~~~~

This library is developed as a helper-library to another piece of software.
What works for that software is also implemented and tested in dictalchemy.

There are bugs and missing features in this library. Please don't hesitate to
register issues at `github <https://github.com/danielholmstrom/dictalchemy>`_.

"""
from __future__ import absolute_import, division

from dictalchemy.classes import DictableModel
from dictalchemy.utils import make_class_dictable, asdict

__all__ = [DictableModel, make_class_dictable, asdict]
