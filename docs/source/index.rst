.. module:: dictalchemy

Dictalchemy
===========

Dictalchemy adds :func:`utils.asdict` and :func:`utils.fromdict` methods to `SQLAlchemy <http://www.sqlalchemy.org/>`_ declarative models.

Currently this works with synonyms and simple relationships as one-to-many and many-to-many. Relationships can be followed in many levels.

Using DictableModel
-------------------

:class:`classes.DictableModel` can be used as base class for `declarative_base` or as a mixin for a declarative class.

Example usage::

    from dictalchemy import DictableModel
    from slqlachemy.ext.declarative import declarative_base
    Base = declarative_base(cls=DictableModel)

Using make_class_dictable()
---------------------------

This method can be run on existing classes to make them dictable.

Example::

    Base = declarative_base()
    make_class_dictable(Base)

Default values
--------------

Default values are defined in :mod:`dictalchemy.constants`.

Using asdict()
--------------

Any collection that inherits from `dict` or `list` is supported together with :class:`sqlalchemy.orm.dynamic.AppenderMixin`, :class:`sqlalchemy.orm.query.Query`  :class:`sqlalchemy.orm.associationproxy._AssociationList` and :class:`sqlalchemy.orm.associationproxy._AssociationDict`.

Simple example::

    >>> session.query(User).asdict()
    {'id': 1, 'username': 'Gerald'}

Using exclude_pk::

    >>> session.query(User).asdict(exclude_pk=True)
    {'username': 'Gerald'}

Using exclude::

    >>> session.query(User).asdict(exclude=['id'])
    {'username': 'Gerald'}

Using follow without arguments::

    >>> session.query(User).asdict(follow={'groups':{}})
    {'username': 'Gerald', groups=[{'id': 1, 'name': 'User'}]}

Using follow with arguments::

    >>> session.query(User).asdict(follow={'groups':{'exclude': ['id']})
    {'username': 'Gerald', groups=[{'name': 'User'}]}

Using follow with a `parent` argument::

    >>> session.query(User).asdict(follow={'groups':{'parent': 'relationships', 'exclude': ['id']})
    {'username': 'Gerald', 'relationships': {'groups':[{'name': 'User'}]}}

Using include(for example for including synonyms/properties)::

    >>> session.query(User).asdict(include=['displayname']
    {'id': 1, 'username': 'Gerald', 'displayname': 'Gerald'}

The `asdict` argument `method`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Note::
  New in v 0.1.2.1

The argument `method` is used to determine which method asdict should call when following relations. If `method` is set in the follow arguments that method will be used instead. See the HAL example in :meth:`dictalchemy.utils.asdict`.

Using fromdict()
----------------

Without arguments::

    >>> user = session.query(User).first()
    >>> dict(user)
    {'id': 3, 'name': 'Gerald'}
    >>> user.fromdict({'name': 'Gerald the Great'})
    >>> dict(user)
    {'name': 'Gerald the Great'}

Excluding underscore::

    >>> user = session.query(User).first()
    >>> dict(user, only=["_secret_id"])
    {'_secret_id': 1}
    >>> user.fromdict({'_secret_id': 2}, exclude_underscore=False)
    >>> dict(user, only=["_secret_id"])
    {'_secret_id': 2}

Updating primary key::

    >>> user = session.query(User).first()
    >>> dict(user, only=["id"])
    {'id': 3}
    >>> user.fromdict({'id': 2}, allow_pk=True)
    >>> dict(user, only=["id"])
    {'id': 2}

Updating relationships::

    >>> dict(user, follow=['address'])
    {'name': 'Gerald the Great', 'address': {'street': None}}
    >>> user.fromdict({'address': {'street': 'Main street'})
    >>> dict(user, follow=['address'])
    {'name': 'Gerald the Great', 'address': {'street': 'Main street'}}

Using include::

    >>> user = session.query(User).first()
    >>> dict(user)
    {'id': 3, 'name': 'Gerald', 'a_synonym': 'Data'}
    >>> user.fromdict({'name': 'Gerald the Great', 'a_synonym': 'Other data'}, include=['a_synonym'])
    >>> dict(user)
    {'name': 'Gerald the Great', 'a_synonym': 'Other data'}

Using only::

    >>> user = session.query(User).first()
    >>> dict(user)
    {'id': 3, 'name': 'Gerald', 'a_synonym': 'Data'}
    >>> user.fromdict({'name': 'Gerald the Great', 'a_synonym': 'Other data'}, only=['name'])
    >>> dict(user)
    {'name': 'Gerald the Great', 'a_synonym': 'Data'}


API
---

.. automodule:: dictalchemy.classes
    :special-members:

.. automodule:: dictalchemy.utils

.. automodule:: dictalchemy.errors

.. automodule:: dictalchemy.constants

Python versions
---------------

Dictalchemy supports python 2.7.3 and python 3.3 through `2to3`. Other versions are not tested.

Source
------

The source is hosted on `http://github.com/danielholmstrom/dictalchemy <http://github.com/danielholmstrom/dictalchemy>`_.

License
-------

dictalchemy is released under the MIT license.

.. toctree::
