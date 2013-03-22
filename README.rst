#####
Intro
#####

Dictalchemy adds asdict() and fromdict() methods to SQLAlchemy declarative models.

Currently this works with synonyms and simple relations-ships as one-to-many and many-to-many. Relationships can be followed in many levels.

The only collections currently supported is sqlalchemy.orm.collections.InstrumentedList and sqlalchemy.orm.collections.MappedCollection.

A more complete documentation can be found on `pypi <http://pythonhosted.org/dictalchemy/dictalchemy.html>`_.

*****
Usage
*****

DictableModel
=============

Mixin dictalchemy.DictableModel in a declarative class or use it as a base class for declarative_base. Each class can have the following attibutes set:

* dictalchemy_exclude: List of properties that should be excluded by default(default empty)
* dictalchemy_exclude_underscore: Exclude properties starting with an underscore(default True)
* dictalchemy_fromdict_allow_pk: If True the primary key may be updated with `fromdict()`
* dictalchemy_asdict_include: List of properties that always should be included when calling `DictableModel.asdict`
* dictalchemy_fromdict\_include: List of properties that always should be included when calling `DictableModel.fromdict`

make_class_dictable()
=====================

This method can be run on existing classes to make them dictable.

Examples
--------

Using asdict::

    >>> from iteralchemy import make_class_dictable
    >>> make_class_dictable(Base)
    >>> user = session.query(User).first()
    >>> dict(user)
    {'id': 3, 'name': 'Gerald'}
    >>> user.asdict(exclude=['id'])
    {'name': 'Gerald'}
    >>> user.asdict(follow=['roles'])
    {'id': 3, 'name': 'Gerald', 'roles': [{'id': 1, 'name': 'admin'}, {'id': 2, 'name': 'user'}]}
    >>> user.asdict(follow={'roles': {'exclude': ['id']})
    {'id': 3, 'name': 'Gerald', 'roles': [{'name': 'admin'}, {'name': 'user'}]}
    >>> user.asdict(follow={'roles': {'exclude': ['id'], 'follow': ['group']})
    {'id': 3, 'name': 'Gerald', 'roles': [{'name': 'admin', 'group': {'id': 1, 'name': 'admin'}}, {'name': 'user', 'group': {'id': 2, 'name': 'user'}}]}

Using fromdict::

    >>> from iteralchemy import make_class_dictable
    >>> make_class_dictable(Base)
    >>> user = session.query(User).first()
    >>> dict(user)
    {'id': 3, 'name': 'Gerald'}
    >>> user.fromdict({'name': 'Gerald the Great'})
    >>> dict(user)
    {'name': 'Gerald the Great'}
    >>> dict(user, follow=['address'])
    {'name': 'Gerald the Great', 'address': {'street': None}}
    >>> user.fromdict({'address': {'street': 'Main street'})
    >>> dict(user, follow=['address'])
    {'name': 'Gerald the Great', 'address': {'street': 'Main street'}}


See dictalchemy/test_asdict.py and dictalchemy/test_asdict for more examples.


License
=======

dictalchemy is released under the MIT license.
