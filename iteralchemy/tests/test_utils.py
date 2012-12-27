# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division

import unittest
from iteralchemy import make_class_iterable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer

engine = create_engine('sqlite:///:memory:', echo=False)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)


class MakeClassIterable(Base):

    __tablename__ = 'makeclassiterable'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __init__(self, name):
        self.name = name


class TestAsdict(unittest.TestCase):

    def setUp(self):
        """ Recreate the database """
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        Base.metadata.drop_all()

    def test_make_class_iterable(self):
        assert not hasattr(MakeClassIterable, 'asdict')
        m = MakeClassIterable('iterable')
        self.session.add(m)
        self.session.commit()

        assert not hasattr(m, 'asdict')
        make_class_iterable(MakeClassIterable)
        assert m.asdict() == {'id': m.id, 'name': m.name}
