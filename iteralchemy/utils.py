# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division

from sqlalchemy.orm import RelationshipProperty, ColumnProperty,\
        SynonymProperty
from sqlalchemy.orm.collections import InstrumentedList

from iteralchemy import constants


def _prepare_arguments(self, exclude=None, exclude_underscore=None,
        follow=None):
    """Prepare values for asdict and fromdict

    :returns: A tuple with prepared values
    """

    if follow == None:
        follow = []
    try:
        follow = dict(follow)
    except ValueError:
        follow = dict.fromkeys(list(follow), {})

    exclude = exclude or []
    exclude += getattr(self, 'asdict_exclude', constants.default_exclude) or []
    if exclude_underscore is None:
        exclude_underscore = getattr(self, 'asdict_exclude_underscore',
                constants.default_exclude_underscore)

    # Get relationships, columns and synonyms
    relations = [k.key for k in self.__mapper__.iterate_properties if
            isinstance(k, RelationshipProperty)]
    columns = [k.key for k in self.__mapper__.iterate_properties if
            isinstance(k, ColumnProperty)]
    synonyms = [k.key for k in self.__mapper__.iterate_properties if
            isinstance(k, SynonymProperty)]

    # Find primary keys
    primary_keys = set()
    for k in self.__mapper__.iterate_properties:
        if hasattr(k, 'columns'):
            for c in k.columns:
                if c.primary_key:
                    primary_keys.add(k.key)

    # TODO: Fix this bug, exclude_underscore is set above, that should be
    # checked there
    if getattr(self, 'asdict_exclude_underscore', True):
        # Exclude everything starting with underscore
        exclude += [k for k in self.__mapper__._props if k[0] == '_']

    return exclude, exclude_underscore, follow, relations, columns, synonyms,\
            primary_keys


def asdict(self, exclude=None, exclude_underscore=None, follow=None):
    """Get a dict from a model

    This method can also be set on a class directly

    :param follow: List or dict of relationships that should be followed.
    If the parameter is a dict the value should be a dict of keyword
    arguments.
    :param exclude: List of properties that should be excluded, will be
    merged with self.asdict_exclude.
    :param exclude_underscore: Overides self.exclude_underscore if set.

    :raises: ValueError if follow contains a non-existent relationship

    :returns: dict
    """

    exclude, exclude_underscore, follow, relations, columns, synonyms,\
            primary_keys =\
        _prepare_arguments(self, exclude, exclude_underscore, follow)

    data = dict([(k, getattr(self, k)) for k in columns + synonyms\
            if k not in exclude])

    for (k, args) in follow.iteritems():
        if k not in relations:
            raise ValueError(\
                    "Key '%r' in parameter 'follow' is not a relations" %\
                    k)
        rel = getattr(self, k)
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

    return data


def fromdict(self, data, exclude=None, exclude_underscore=None, follow=None):

    exclude, exclude_underscore, follow, relations, columns, synonyms,\
            primary_keys =\
            _prepare_arguments(self, exclude, exclude_underscore, follow)

    # Update simple data
    for k, v in data.iteritems():
        if k in primary_keys:
            raise Exception("Primary keys(%r) cannot be updated by fromdict" % k)
        if k in columns:
            setattr(self, k, v)


def make_class_iterable(cls, exclude=constants.default_exclude,
        exclude_underscore=constants.default_exclude_underscore):
    """Make a class iterable

    Useful for when the Base class is already defined, for example when using
    Flask-SQLAlchemy.

    Warning: This method will overwrite existing attributes if they exists.

    :param exclude: Will be set as asdict_exclude on the class
    :param exclud_underscore: Will be set as asdict_exclude_underscore on the
    class

    :returns: The class
    """

    setattr(cls, 'asdict_exclude', exclude)
    setattr(cls, 'asdict_exclude_underscore', exclude_underscore)
    setattr(cls, 'asdict', asdict)
    return cls
