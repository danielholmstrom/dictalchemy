# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division
from iteralchemy.tests import TestCase, Named, NamedOtherColumnName,\
        NamedWithSynonym, OneToManyChild, OneToManyParent,\
        M2mLeft, M2mRight


class TestAsdict(TestCase):

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
