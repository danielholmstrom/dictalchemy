# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division

from sqlalchemy.orm import RelationshipProperty, ColumnProperty,\
        SynonymProperty
from sqlalchemy.orm.collections import InstrumentedList


class IterableModel(object):
    """Adds iteration and asdict() method to an sqlalchemy class

    """

    asdict_exclude = None
    """List of properties that always will be excluded"""
    asdict_exclude_underscore = True
    """Exclude properties starting with underscore"""

    def asdict(self, exclude=None, exclude_underscore=None, follow=None):
        """Get a dict from a model


        :param follow: List or dict of relationships that should be followed.
        If the parameter is a dict the value should be a dict of keyword
        arguments.
        :param exclude: List of properties that should be excluded, will be
        merged with self.asdict_exclude
        :param exclude_underscore: Overides self.exclude_underscore if set

        :raises: ValueError if follow contains a non-existent relationship

        :returns: dict
        """

        if follow == None:
            follow = []
        try:
            follow = dict(follow)
        except ValueError:
            follow = dict.fromkeys(list(follow), {})


        exclude = exclude or []
        exclude += self.asdict_exclude or []
        if exclude_underscore is None:
            exclude_underscore = self.asdict_exclude_underscore


        # Get relationships, columns and synonyms
        relations = [k.key for k in self.__mapper__.iterate_properties if
                isinstance(k, RelationshipProperty)]
        columns = [k.key for k in self.__mapper__.iterate_properties if
                isinstance(k, ColumnProperty)]
        synonyms = [k.key for k in self.__mapper__.iterate_properties if
                isinstance(k, SynonymProperty)]

        if self.asdict_exclude_underscore:
            # Exclude everything starting with underscore
            exclude += [k for k in self.__mapper__._props if k[0] == '_']

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

    def __iter__(self):
        """Iterates

        yields tuples that can be used to create a dict
        """
        for i in self.asdict().iteritems():
            yield i
