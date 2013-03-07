# vim: set fileencoding=utf-8 :
"""

************
Introduction
************

This library adds basic functionality for getting a dict from an SQLAlchemy
model and updating a model from a dict.

SQLAlchemy is a very complex library. It contains synonyms, lists, sets, mixins
and god knows what. Automatically convert that to a dict or update from a
dict is not a simple task. This library should not be used on more complex
models without thorough testing, it should however be fine to use on simple
models.

Usage
=====

There are two ways to use dictalchemy. Either by using
:class:`dictalchemy.classes.DictableModel` as base class or by using
:meth:`dictalchemy.utils.make_class_dictable` on an existing base class.

The actual work is done in the functions :func:`dictalchemy.utils.asdict` and
:func:`dictalchemy.utils.fromdict`.

Since attributes are checked on instances each instance can get their own setup
of rules. This can be useful when returning a model instance as a response. If
default values are set on that specific instance calling `dict` will render it
properly.

Using DictableModel
-----------------------------------------

Use :class:`dictalchemy.classes.DictableModel` as a base class for
:class:`sqlalchemy.ext.declarative_base`.

Example::

    from sqlalchemy.ext import declarative_base
    from dictalchemy import DictableModel
    Base = declarative_base(cls=DictableModel)

Using make_class_dictable
-------------------------

:func:`dictalchemy.utils.make_class_dictable` adds methods and attributes to an
already existing class

Example::

    from sqlalchemy.ext import declarative_base
    from dictalchemy import make_class_dictable
    base = declarative_base()
    make_class_dictable(base)

Attributes and parameters
-------------------------

Dictalchemy uses some basic attributes and parameters to convert to and from
dict. The most basic are:

* include
* exclude
* exclude_pk
* allow_pk
* follow
* only

The defaults varies depending on the flag. For example, allow_pk will by
default be set to True for fromdict and exclude_pk will be set to False in
asdict.

A class or model can have these attributes set, prefixed with
*dictalchemy\_*. Some of them can also be overridden depending on if
:meth:`dictalchemy.utils.asdict` or :meth:`dictalchemy.utils.fromdict` is
called. If they are set they will override the more basic attribute.

Some semi-rules
^^^^^^^^^^^^^^^

* In general `include` flags will override `exclude` flags.
* In general `only` will override `exclude` and `include` flags.
* In :meth:`dictalchemy.utils.fromdict` `allow_pk`=False will override all \
        other flags.


Class/Model attributes
^^^^^^^^^^^^^^^^^^^^^^

* dictalchemy_exclude
* dictalchemy_include
* dictalchemy_fromdict_include
* dictalchemy_asdict_include
* dictalchemy_exclude_underscore
* dictalchemy_fromdict_allow_pk


A note about synonyms
=====================

Synonyms wraps a reader and a writer method. These methods can do whatever they
want to so there is no way to safely updated data with synonyms. So keep in
mind that using synonyms will make it possible to circumvent for example
dictalchemy_exclude_pk.

Bugs and missing features
=========================

This library is developed as a helper-library to another piece of software.
What works for that software is also implemented and tested in dictalchemy.

There are bugs and missing features in this library. Please don't hesitate to
register issues at `github <https://github.com/danielholmstrom/dictalchemy>`_.

"""
from __future__ import absolute_import, division

from dictalchemy.classes import DictableModel
from dictalchemy.utils import make_class_dictable, asdict
from dictalchemy.errors import (DictalchemyError, UnsupportedRelationError,
                                MissingRelationError)

__all__ = [DictableModel,
           make_class_dictable,
           asdict,
           DictalchemyError,
           UnsupportedRelationError,
           MissingRelationError]
