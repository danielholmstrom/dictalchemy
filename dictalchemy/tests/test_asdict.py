# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division
from dictalchemy.tests import (
    TestCase,
    Named,
    NamedOtherColumnName,
    NamedWithSynonym,
    OneToManyChild,
    OneToManyParent,
    M2mLeft,
    M2mRight,
    MultipleChildParent,
    MultipleChildChild1,
    MultipleChildChild2,
    MultipleChildChild1Child,
    WithHybrid,
    WithDefaultInclude,
    WithAttributeMappedCollection,
    WithAttributeMappedCollectionChild,
    DynamicRelationChild,
    DynamicRelationParent,
    ParentWithOptionalChild,
    OptionalChild,
    WithHalChild,
    WithHalParent,
)


class TestAsdict(TestCase):

    def _setup_multiple_child(self):
        s = self.session
        p = MultipleChildParent('parent')
        c1 = MultipleChildChild1('child1')
        c2 = MultipleChildChild2('child2')
        p.child1 = c1
        p.child2 = c2
        s.add(p)
        s.commit()
        return p, c1, c2

    def _setup_multiple_child_child(self):
        p, c1, c2 = self._setup_multiple_child()
        s = self.session
        c1c = MultipleChildChild1Child('child1child')
        c1.child = c1c
        s.add(c1)
        s.commit()
        return p, c1, c2, c1c

    def test_dict(self):
        named = Named('a name')
        named.asdict() == dict(named)

    def test_exclude_flag(self):
        named = Named('a name')
        assert named.asdict(exclude=['id']) == {'name': 'a name'}

    def test_exclude_pk(self):
        named = Named('a name')
        self.session.add(named)
        self.session.commit()
        assert named.asdict(exclude_pk=True) == {'name': named.name}

    def test_named_without_save(self):
        named = Named('a name')
        assert named.asdict() == {'id': None, 'name': named.name}

    def test_named_with_save(self):
        named = Named('a name')
        self.session.add(named)
        self.session.commit()
        assert named.asdict() == {'id': named.id, 'name': named.name}

    def test_named_other_columnname(self):
        named = NamedOtherColumnName('a name')
        assert named.asdict() == {'id': None, 'name': named.name}

    def test_named_synonym(self):
        named = NamedWithSynonym('a name')
        assert named.asdict() == {'id': None, 'name': named.name}

    def test_one_to_many_plain(self):
        child = OneToManyChild('child')
        parent = OneToManyParent('parent')
        parent.child = child
        self.session.add(parent)
        self.session.commit()
        assert parent.asdict() == {'id': parent.id, 'name': parent.name}

    def test_one_to_many_follow(self):
        child = OneToManyChild('child')
        parent = OneToManyParent('parent')
        parent.child = child
        self.session.add(parent)
        self.session.commit()
        assert parent.asdict(follow=['child']) == {'id': parent.id,
                                                   'name': parent.name,
                                                   'child': child.asdict()}

    def test_many_to_many_follow(self):
        s = self.session
        l1 = M2mLeft('l1')
        r1 = M2mRight('r1')
        r2 = M2mRight('r2')
        l1.rights.append(r1)
        l1.rights.append(r2)
        s.add(l1)
        s.commit()
        assert l1.asdict(follow=['rights']) == {'id': l1.id,
                                                'name': l1.name,
                                                'rights': [r1.asdict(),
                                                           r2.asdict()]}
        assert r1.asdict(follow=['lefts']) == {'id': r1.id,
                                               'name': r1.name,
                                               'lefts': [l1.asdict()]}

    def test_one_to_many_follow_with_arguments(self):
        s = self.session
        l1 = M2mLeft('l1')
        r1 = M2mRight('r1')
        r2 = M2mRight('r2')
        l1.rights.append(r1)
        l1.rights.append(r2)
        s.add(l1)
        s.commit()
        assert l1.asdict(follow={'rights': {'exclude': ['id']}}
                         ) == {'id': l1.id,
                               'name': l1.name,
                               'rights': [{'name': r1.name},
                                          {'name': r2.name}]}
        assert r1.asdict(follow={'lefts': {'exclude': ['id']}}
                         ) == {'id': r1.id,
                               'name': r1.name,
                               'lefts': [{'name': l1.name}]}

    def test_multiple_child_follow_only_one(self):
        p, c1, c2 = self._setup_multiple_child()
        assert p.asdict(follow=['child1']) == {'id': p.id,
                                               'name': p.name,
                                               'child1': {'id': c1.id,
                                                          'name': c1.name}}

    def test_multiple_child_follow_two_with_different_arguments(self):
        p, c1, c2 = self._setup_multiple_child()
        assert p.asdict(follow={'child1': {},
                                'child2': {'exclude': ['id']}}
                        ) == {'id': p.id,
                              'name': p.name,
                              'child1': {'id': c1.id,
                                         'name': c1.name},
                              'child2': {'name': c2.name}}

    def test_multiple_child_follow_two_levels(self):
        p, c1, c2, c1c = self._setup_multiple_child_child()
        assert p.asdict(follow={'child1': {'follow': ['child']}}
                        ) == {'id': p.id,
                              'name': p.name,
                              'child1': {'id': c1.id,
                                         'name': c1.name,
                                         'child': {'id': c1c.id,
                                                   'name': c1c.name}}}

    def test_multiple_child_follow_two_levels_with_arguments(self):
        p, c1, c2, c1c = self._setup_multiple_child_child()
        assert p.asdict(follow={'child1': {'follow':
                                           {'child': {'exclude': ['id']}}}}
                        ) == {'id': p.id,
                              'name': p.name,
                              'child1': {'id': c1.id,
                                         'name': c1.name,
                                         'child': {'name': c1c.name}}}

    def test_hybrid_property(self):
        assert WithHybrid(2).asdict(include=['id']) == {'id': 2}

    def test_default_include(self):
        assert WithDefaultInclude(2).asdict() == {'id': 2, 'id_alias': 2}

    def test_dictalchemy_include(self):
        m = WithHybrid(2)
        assert 'id' not in dict(m)
        setattr(m, 'dictalchemy_include', ['id'])
        assert 'id' in dict(m)

    def test_dictalchemy_asdict_include_overrides(self):
        m = WithHybrid(2)
        assert 'id' not in dict(m)
        setattr(m, 'dictalchemy_include', ['id'])
        assert 'id' in dict(m)
        setattr(m, 'dictalchemy_asdict_include', [])
        assert 'id' not in dict(m)

    def test_attribute_mapped_collection(self):
        p = WithAttributeMappedCollection()
        p.childs['child1'] = WithAttributeMappedCollectionChild('child1')
        assert p.asdict(follow=['childs']) == {'childs':
                                               {'child1':
                                                {'parent_id': None,
                                                 'id': None,
                                                 'name': 'child1'}},
                                               'id': None}

    def test_only(self):
        named = Named('a name')
        assert 'name' in dict(named)
        assert 'id' in dict(named)
        assert 'name' not in named.asdict(only=['id'])
        assert 'id' not in named.asdict(only=['name'])

    def test_only_overrides_include(self):
        named = Named('a name')
        assert 'name' in dict(named)
        assert 'id' in dict(named)
        assert 'name' not in named.asdict(only=['id'], include=['name'])
        assert 'id' not in named.asdict(only=['name'], include=['id'])

    def test_only_overrides_exclude(self):
        named = Named('a name')
        assert 'name' in dict(named)
        assert 'id' in dict(named)
        assert 'name' not in named.asdict(only=['id'], exclude=['id'])
        assert 'id' not in named.asdict(only=['name'], exclude=['name'])

    def test_dynamic_relation(self):

        child = DynamicRelationChild()
        parent = DynamicRelationParent()
        parent.childs.append(child)
        self.session.add(parent)
        self.session.add(child)
        self.session.commit()
        child_id = child.id
        parent_id = parent.id
        self.session.expire_all()
        parent = self.session.query(DynamicRelationParent
                                    ).filter_by(id=parent_id).first()
        assert parent.asdict(follow={'childs':{}}
                             )['childs'][0]['id'] == child_id

    def test_nullable_fk_returns_none_relation(self):
        parent = ParentWithOptionalChild()
        self.session.add(parent)
        self.session.commit()
        assert parent.asdict(follow={'child':{}})['child'] == None
        child = OptionalChild()
        parent.child = child
        self.session.add(child)
        self.session.commit()
        assert parent.asdict(follow={'child':{}})['child']['id'] == child.id

    def test_method_argument(self):

        parent = WithHalParent()
        self.session.add(parent)
        self.session.commit()

        assert parent.ashal() == {
            'id': parent.id,
            'child_id': None,
            '_embedded': {},
            '_links': {
                'self': '/with_hal_parent/{0}'.format(parent.id),
            },
        }

        child = WithHalChild()
        parent.child = child
        self.session.add(child)
        self.session.commit()

        result = parent.ashal(follow={'child': {'_embedded': True}})
        expected = {
            'id': parent.id,
            'child_id': child.id,
            '_embedded': {
                'child': {
                    'id': child.id,
                    '_embedded': {},
                    '_links': {
                        'self': '/with_hal_child/{0}'.format(child.id),
                    },
                }
            },
            '_links': {
                'self': '/with_hal_parent/{0}'.format(parent.id),
            },
        }

        assert result == expected

        # Using `method` argument when following child
        result = parent.ashal(follow={'child': {'_embedded': True,
                                                'method': 'asdict'}})
        expected = {
            'id': parent.id,
            'child_id': child.id,
            '_embedded': {
                'child': {
                    'id': child.id,
                }
            },
            '_links': {
                'self': '/with_hal_parent/{0}'.format(parent.id),
            },
        }
