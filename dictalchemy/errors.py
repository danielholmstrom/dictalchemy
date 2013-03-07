# vim: set fileencoding=utf-8 :
"""
~~~~~~
Errors
~~~~~~

"""
from __future__ import absolute_import, division


class DictalchemyError(Exception):
    """Base class for Dictalchemy errors"""
    pass


class UnsupportedRelationError(DictalchemyError):
    """Raised when a relation is not supported by asdict or fromdict.

    The name of the relation can be accessed from 'relation_key'
    """

    def __init__(self, relation_key):
        self.relation_key = relation_key

    def __str__(self):
        return "Relation '%r' is not supported" % (self.relation_key,)


class MissingRelationError(DictalchemyError):
    """Raised when a relationship is missing

    The name of the relation can be accessed from 'relation_key'
    """

    def __init__(self, relation_key):
        self.relation_key = relation_key

    def __str__(self):
        return "Relation '%r' is not found" % (self.relation_key,)
