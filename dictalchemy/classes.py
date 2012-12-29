# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division

from dictalchemy import utils

class DictableModel(object):
    """Adds iteration and asdict() method to an sqlalchemy class.

    :ivar asdict_exclude: List of properties that should always be excluded.
    :ivar asdict_exclude_underscore: If True properties starting with an \
            underscore will always be excluded.

    """

    asdict = utils.asdict

    fromdict = utils.fromdict

    def __iter__(self):
        """Iterates

        Yields tuples that can be used to create a dict.

        """
        for i in self.asdict().iteritems():
            yield i
