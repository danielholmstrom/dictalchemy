# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division

from iteralchemy import utils

class IterableModel(object):
    """Adds iteration and asdict() method to an sqlalchemy class

    Classproperties that can be defined:

    asdict_exclude: List of properties that should always be excluded.
    asdict_exclude_underscore: If True properties starting with an underscore
    will always be excluded.
    """

    asdict = utils.asdict

    def __iter__(self):
        """Iterates

        yields tuples that can be used to create a dict
        """
        for i in self.asdict().iteritems():
            yield i
