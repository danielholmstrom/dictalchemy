# vim: set fileencoding=utf-8 :
"""
~~~~~~~~~
Utilities
~~~~~~~~~
"""
from __future__ import absolute_import, division

from sqlalchemy.orm import (RelationshipProperty, ColumnProperty,
                            SynonymProperty)
from sqlalchemy.orm.collections import InstrumentedList, MappedCollection
from sqlalchemy.orm.dynamic import AppenderMixin
from sqlalchemy.orm.query import Query

from dictalchemy import constants
from dictalchemy import errors


def get_relation_keys(model):
    """Get relation keys for a model

    :returns: List of RelationProperties
    """
    return [k.key for k in model.__mapper__.iterate_properties if
            isinstance(k, RelationshipProperty)]


def get_column_keys(model):
    """Get column keys for a model

    :returns: List of column keys
    """
    return [k.key for k in model.__mapper__.iterate_properties if
            isinstance(k, ColumnProperty)]


def get_synonym_keys(model):
    """Get synonym keys for a model

    :returns: List of keys for synonyms
    """
    return [k.key for k in model.__mapper__.iterate_properties if
            isinstance(k, SynonymProperty)]


def get_primary_key_properties(model):
    """Get the column properties that affects a primary key

    :returns: Set of column keys
    """
    # Find primary keys
    primary_keys = set()
    for k in model.__mapper__.iterate_properties:
        if hasattr(k, 'columns'):
            for c in k.columns:
                if c.primary_key:
                    primary_keys.add(k.key)
    return primary_keys


def asdict(model, exclude=None, exclude_underscore=None, exclude_pk=None,
           follow=None, include=None, only=None):
    """Get a dict from a model

    :param follow: List or dict of relationships that should be followed. \
            If the parameter is a dict the value should be a dict of \
            keyword arguments. Currently it follows InstrumentedList,\
            MappedCollection and regular 1:1, 1:m, m:m relationships.
    :param exclude: List of properties that should be excluded, will be \
            merged with `model.dictalchemy_exclude`
    :param exclude_pk: If True any column that refers to the primary key will \
            be excluded.
    :param exclude_underscore: Overides `model.dictalchemy_exclude_underscore`\
            if set
    :param include: List of properties that should be included. Use this to \
            allow python properties to be called. This list will be merged \
            with `model.dictalchemy_asdict_include` or \
            `model.dictalchemy_include`.
    :param only: List of properties that should be included. This will \
            override everything else except `follow`.

    :raises: :class:`dictalchemy.errors.MissingRelationError` \
            if `follow` contains a non-existent relationship.
    :raises: :class:`dictalchemy.errors.UnsupportedRelationError` If `follow` \
            contains an existing relationship that currently isn't supported.

    :returns: dict

    """

    if follow is None:
        follow = []
    try:
        follow = dict(follow)
    except ValueError:
        follow = dict.fromkeys(list(follow), {})

    columns = get_column_keys(model)
    synonyms = get_synonym_keys(model)
    relations = get_relation_keys(model)

    if only:
        attrs = only
    else:
        exclude = exclude or []
        exclude += getattr(model, 'dictalchemy_exclude',
                           constants.default_exclude) or []
        if exclude_underscore is None:
            exclude_underscore = getattr(model,
                                         'dictalchemy_exclude_underscore',
                                         constants.default_exclude_underscore)
        if exclude_underscore:
            # Exclude all properties starting with underscore
            exclude += [k.key for k in model.__mapper__.iterate_properties
                        if k.key[0] == '_']
        if exclude_pk is True:
            exclude += get_primary_key_properties(model)

        include = (include or []) + (getattr(model,
                                             'dictalchemy_asdict_include',
                                             getattr(model,
                                                     'dictalchemy_include',
                                                     None)) or [])
        attrs = [k for k in columns + synonyms + include if k not in exclude]

    data = dict([(k, getattr(model, k)) for k in attrs])

    for (k, args) in follow.iteritems():
        if k not in relations:
            raise errors.MissingRelationError(k)
        rel = getattr(model, k)
        if hasattr(rel, 'asdict'):
            data.update({k: rel.asdict(**args)})
        elif isinstance(rel, InstrumentedList):
            children = []
            for child in rel:
                if hasattr(child, 'asdict'):
                    children.append(child.asdict(**args))
                else:
                    children.append(dict(child))
            data.update({k: children})
        elif isinstance(rel, MappedCollection):
            children = {}
            for (child_key, child) in rel.iteritems():
                if hasattr(child, 'asdict'):
                    children[child_key] = child.asdict(**args)
                else:
                    children[child_key] = child.dict(child)
            data.update({k: children})
        elif isinstance(rel, (AppenderMixin, Query)):
            children = []
            for child in rel.all():
                if hasattr(child, 'asdict'):
                    children.append(child.asdict(**args))
                else:
                    children.append(dict(child))
            data.update({k: children})
        else:
            raise errors.UnsupportedRelationError(k)

    return data


def fromdict(model, data, exclude=None, exclude_underscore=None,
             allow_pk=None, follow=None, include=None, only=None):
    """Update a model from a dict

    Works almost identically as :meth:`dictalchemy.utils.asdict`. However, it
    will not create missing instances or update collections.

    This method updates the following properties on a model:

    * Simple columns
    * Synonyms
    * Simple 1-m relationships

    :param data: dict of data
    :param exclude: list of properties that should be excluded
    :param exclude_underscore: If True underscore properties will be excluded,\
            if set to None model.dictalchemy_exclude_underscore will be used.
    :param allow_pk: If True any column that refers to the primary key will \
            be excluded. Defaults model.dictalchemy_fromdict_allow_pk or \
            dictable.constants.fromdict_allow_pk. If set to True a primary \
            key can still be excluded with the `exclude` parameter.
    :param follow: Dict of relations that should be followed, the key is the \
            arguments passed to the relation. Relations only works on simple \
            relations, not on lists.
    :param include: List of properties that should be included. This list \
            will override anything in the exclude list. It will not override \
            allow_pk.
    :param only: List of the only properties that should be returned. This \
            will not override `allow_pk` or `follow`.

    :raises: :class:`dictalchemy.errors.DictalchemyError` If a primary key is \
            in data and allow_pk is False

    :returns: The model

    """

    if follow is None:
        follow = []
    try:
        follow = dict(follow)
    except ValueError:
        follow = dict.fromkeys(list(follow), {})

    columns = get_column_keys(model)
    synonyms = get_synonym_keys(model)
    relations = get_relation_keys(model)
    primary_keys = get_primary_key_properties(model)

    if only:
        attrs = only
    else:
        exclude = exclude or []
        exclude += getattr(model, 'dictalchemy_exclude',
                           constants.default_exclude) or []
        if exclude_underscore is None:
            exclude_underscore = getattr(model,
                                         'dictalchemy_exclude_underscore',
                                         constants.default_exclude_underscore)

        if exclude_underscore:
            # Exclude all properties starting with underscore
            exclude += [k.key for k in model.__mapper__.iterate_properties
                        if k.key[0] == '_']

        if allow_pk is None:
            allow_pk = getattr(model, 'dictalchemy_fromdict_allow_pk',
                               constants.default_fromdict_allow_pk)

        include = (include or []) + (getattr(model,
                                             'dictalchemy_fromdict_include',
                                             getattr(model,
                                                     'dictalchemy_include',
                                                     None)) or [])
        attrs = [k for k in columns + synonyms if k not in exclude] + include

    # Update simple data
    for k, v in data.iteritems():
        if not allow_pk and k in primary_keys:
            msg = "Primary key(%r) cannot be updated by fromdict."
            "Set 'dictalchemy_fromdict_allow_pk' to True in your Model"
            " or pass 'allow_pk=True'." % k
            raise errors.DictalchemyError(msg)
        if k in attrs:
            setattr(model, k, v)

    # Update simple relations
    for (k, args) in follow.iteritems():
        if k not in data:
            continue
        if k not in relations:
            raise errors.MissingRelationError(k)
        rel = getattr(model, k)
        # TODO: Check for fromdict, not asdict
        if hasattr(rel, 'asdict'):
            rel.fromdict(data[k], **args)

    return model


def iter(model):
    """iter method for models

    Yields everything returned by `asdict`.
    """
    for i in model.asdict().iteritems():
        yield i


def make_class_dictable(
        cls,
        exclude=constants.default_exclude,
        exclude_underscore=constants.default_exclude_underscore,
        fromdict_allow_pk=constants.default_fromdict_allow_pk,
        include=None,
        asdict_include=None,
        fromdict_include=None):
    """Make a class dictable

    Useful for when the Base class is already defined, for example when using
    Flask-SQLAlchemy.

    Warning: This method will overwrite existing attributes if they exists.

    :param exclude: Will be set as dictalchemy_exclude on the class
    :param exclude_underscore: Will be set as dictalchemy_exclude_underscore \
            on the class
    :param fromdict_allow_pk: Will be set as dictalchemy_fromdict_allow_pk\
            on the class
    :param include: Will be set as dictalchemy_include on the class.
    :param asdict_include: Will be set as `dictalchemy_asdict_include` on the \
            class. If not None it will override `dictalchemy_include`.
    :param fromdict_include: Will be set as `dictalchemy_fromdict_include` on \
            the class. If not None it will override `dictalchemy_include`.

    :returns: The class
    """

    setattr(cls, 'dictalchemy_exclude', exclude)
    setattr(cls, 'dictalchemy_exclude_underscore', exclude_underscore)
    setattr(cls, 'dictalchemy_fromdict_allow_pk', fromdict_allow_pk)
    setattr(cls, 'asdict', asdict)
    setattr(cls, 'fromdict', fromdict)
    setattr(cls, '__iter__', iter)
    setattr(cls, 'dictalchemy_include', include)
    setattr(cls, 'dictalchemy_asdict_include', asdict_include)
    setattr(cls, 'dictalchemy_fromdict_include', fromdict_include)
    return cls
