# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division

from dictalchemy import utils


class DictableModel(object):
    """Adds iteration and asdict() method to an sqlalchemy class.

    :ivar dictalchemy_exclude: List of properties that should always be \
            excluded.
    :ivar dictalchemy_exclude_underscore: If True properties starting with an \
            underscore will always be excluded.
    :ivar dictalchemy_fromdict_allow_pk: If True the primary key can be \
            updated by :meth:`dictalchemy.fromdict`.

    """

    asdict = utils.asdict

    fromdict = utils.fromdict

    __iter__ = utils.iter
