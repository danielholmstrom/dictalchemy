# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division
from iteralchemy.tests import TestCase, Named, NamedOtherColumnName,\
        NamedWithSynonym, OneToManyChild, OneToManyParent,\
        M2mLeft, M2mRight,\
        MultipleChildParent, MultipleChildChild1, MultipleChildChild2


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

    def test_dict(self):
        named = Named('a name')
        named.asdict() == dict(named)

    def test_exclude_flag(self):
        named = Named('a name')
        assert named.asdict(exclude=['id']) == {'name': 'a name'}

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
        assert parent.asdict(follow=['child']) ==\
                {'id': parent.id, 'name': parent.name,
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
        assert l1.asdict(follow=['rights']) == {'id': l1.id, 'name': l1.name,
                'rights': [r1.asdict(), r2.asdict()]}
        assert r1.asdict(follow=['lefts']) == {'id': r1.id, 'name': r1.name,
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
        assert l1.asdict(follow={'rights': {'exclude': ['id']}}) ==\
                {'id': l1.id, 'name': l1.name,
                    'rights': [{'name': r1.name}, {'name': r2.name}]}
        assert r1.asdict(follow={'lefts': {'exclude': ['id']}}) ==\
                {'id': r1.id, 'name': r1.name,
                    'lefts': [{'name': l1.name}]}

    def test_multiple_child_follow_only_one(self):
        p, c1, c2 = self._setup_multiple_child()
        assert p.asdict(follow=['child1']) == {'id': p.id, 'name': p.name,
                'child1': {'id': c1.id, 'name': c1.name}}

    def test_multiple_child_follow_two_with_different_arguments(self):
        p, c1, c2 = self._setup_multiple_child()
        assert p.asdict(follow={'child1': {},
            'child2': {'exclude': ['id']}}) ==\
                    {'id': p.id, 'name': p.name,
                'child1': {'id': c1.id, 'name': c1.name},
                'child2': {'name': c2.name}}
