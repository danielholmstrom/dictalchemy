# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division

from dictalchemy import DictableModel
from dictalchemy.utils import arg_to_dict
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref, synonym
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.collections import attribute_mapped_collection


# Setup sqlalchemy
engine = create_engine('sqlite:///:memory:', echo=False)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine, cls=DictableModel)


class TestCase(unittest.TestCase):

    def setUp(self):
        """ Recreate the database """
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        Base.metadata.drop_all()


class Named(Base):
    __tablename__ = 'named'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class NamedWithOtherPk(Base):
    __tablename__ = 'namedwithotherpk'
    id = Column('other_id', Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class NamedOtherColumnName(Base):
    __tablename__ = 'named_with_other_column'

    id = Column(Integer, primary_key=True)
    name = Column('namecolumn', String)

    def __init__(self, name):
        self.name = name


class NamedWithSynonym(Base):
    __tablename__ = 'named_with_synonym'

    id = Column(Integer, primary_key=True)
    _name = Column(String)

    def _setname(self, name):
        self._name = name

    def _getname(self):
        return self._name

    name = synonym('_name', descriptor=property(_getname, _setname))

    def __init__(self, name):
        self.name = name


class OneToManyChild(Base):

    __tablename__ = 'onetomanychild'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __init__(self, name):
        self.name = name


class OneToManyParent(Base):

    __tablename__ = 'onetomanyparent'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    _child_id = Column(Integer, ForeignKey(OneToManyChild.id))

    child = relationship(OneToManyChild,
                         primaryjoin=_child_id == OneToManyChild.id,
                         backref=backref('parent'))

    def __init__(self, name):
        self.name = name


m2m_table = Table('m2m_table',
                  Base.metadata,
                  Column('left_id', Integer,
                         ForeignKey('m2mleft.id'),
                         primary_key=True),
                  Column('right_id', Integer,
                         ForeignKey('m2mright.id'),
                         primary_key=True),
                  )


class M2mLeft(Base):
    __tablename__ = 'm2mleft'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __init__(self, name):
        self.name = name

    rights = relationship('M2mRight',
                          secondary=m2m_table,
                          backref=backref('lefts'))


class M2mRight(Base):
    __tablename__ = 'm2mright'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __init__(self, name):
        self.name = name


class MultipleChildChild1Child(Base):

    __tablename__ = 'multiplechildchild1child'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __init__(self, name):
        self.name = name


class MultipleChildChild1(Base):

    __tablename__ = 'multiplechildchild1'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    _child_id = Column(Integer, ForeignKey(MultipleChildChild1Child.id))

    child = relationship(MultipleChildChild1Child,
                         primaryjoin=_child_id == MultipleChildChild1Child.id,
                         backref=backref('parent'))

    def __init__(self, name):
        self.name = name


class MultipleChildChild2(Base):

    __tablename__ = 'multiplechildchild2'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __init__(self, name):
        self.name = name


class MultipleChildParent(Base):

    __tablename__ = 'multiplechildparent'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    _child1_id = Column(Integer, ForeignKey(MultipleChildChild1.id))

    _child2_id = Column(Integer, ForeignKey(MultipleChildChild2.id))

    child1 = relationship(MultipleChildChild1,
                          primaryjoin=_child1_id == MultipleChildChild1.id,
                          backref=backref('parent'))

    child2 = relationship(MultipleChildChild2,
                          primaryjoin=_child2_id == MultipleChildChild2.id,
                          backref=backref('parent'))

    def __init__(self, name):
        self.name = name


class WithHybrid(Base):

    __tablename__ = 'withhybrid'

    _id = Column('id', Integer, primary_key=True)

    @hybrid_property
    def id(self):
        return self._id

    @id.setter
    def set_id(self, value):
        self._id = value

    def __init__(self, id):
        self.id = id


class WithDefaultInclude(Base):

    __tablename__ = 'withdefaultinclude'

    dictalchemy_include = ['id_alias']

    id = Column('id', Integer, primary_key=True)

    @hybrid_property
    def id_alias(self):
        return self.id

    @id_alias.setter
    def set_id_alias(self, value):
        self.id = value

    def __init__(self, id):
        self.id = id


class WithAttributeMappedCollectionChild(Base):

    __tablename__ = 'withattributemappedcollectionchild'

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)

    parent_id = Column(Integer, ForeignKey('withattributemappedcollection.id'))

    def __init__(self, name):
        self.name = name


class WithAttributeMappedCollection(Base):

    __tablename__ = 'withattributemappedcollection'

    id = Column(Integer, primary_key=True)

    childs = relationship(WithAttributeMappedCollectionChild,
                          collection_class=attribute_mapped_collection('name'),
                          cascade="all, delete-orphan",
                          backref=backref('parents'))


class DynamicRelationChild(Base):

    __tablename__ = 'dynamicrelationchild'

    id = Column(Integer, primary_key=True)

    parent_id = Column(Integer, ForeignKey('dynamicrelationparent.id'),
                       nullable=False)


class DynamicRelationParent(Base):

    __tablename__ = 'dynamicrelationparent'

    id = Column(Integer, primary_key=True)

    childs = relationship(
        DynamicRelationChild,
        primaryjoin="DynamicRelationChild.parent_id==DynamicRelationParent.id",
        backref=backref('parent'),
        lazy='dynamic')


class OptionalChild(Base):
    __tablename__ = 'optionalchild'
    id = Column(Integer, primary_key=True)


class ParentWithOptionalChild(Base):
    __tablename__ = 'parentwithoptionalchild'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('optionalchild.id'), nullable=True)
    child = relationship(OptionalChild, uselist=False)


class AsHalMixin(object):

    base_url = None

    def get_hal_links(self):
        if self.base_url:
            return {'self': '{0}/{1}'.format(self.base_url, self.id)}
        else:
            return {}

    def ashal(self, **kwargs):
        kwargs['method'] = 'ashal'
        result = self.asdict(**kwargs)

        follow = arg_to_dict(kwargs.get('follow', None))
        _embedded = {}
        for (k, args) in follow.iteritems():
            if args.get('_embedded', None) and k in result:
                _embedded[k] = result.pop(k)

        result['_embedded'] = _embedded
        result['_links'] = self.get_hal_links()

        return result


class WithHalChild(Base, AsHalMixin):

    __tablename__ = 'withhalchild'

    base_url = '/with_hal_child'

    id = Column(Integer, primary_key=True)


class WithHalParent(Base, AsHalMixin):

    __tablename__ = 'withhalparent'

    base_url = '/with_hal_parent'

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('withhalchild.id'), nullable=True)
    child = relationship(WithHalChild)
