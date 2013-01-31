# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division

# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division
from dictalchemy.tests import TestCase, Named, NamedWithOtherPk,\
        NamedOtherColumnName,\
        NamedWithSynonym, OneToManyChild, OneToManyParent,\
        M2mLeft, M2mRight,\
        MultipleChildParent, MultipleChildChild1, MultipleChildChild2,\
        MultipleChildChild1Child, WithHybrid, WithDefaultInclude


class TestFromdict(TestCase):

    def test_simple(self):
        s = self.session
        named = Named('a name')
        s.add(named)
        s.commit()
        new = {'name': 'other name'}
        named.fromdict(new)
        assert named.asdict() == {'id': named.id, 'name': new['name']}

    def test_simple_aborts_on_pk(self):
        s = self.session
        named = Named('a name')
        s.add(named)
        s.commit()
        new = {'id': 7}
        try:
            named.fromdict(new)
        except:
            pass
        else:
            assert False

    def test_fromdict_allow_pk(self):
        s = self.session
        named = Named('a name')
        s.add(named)
        s.commit()
        new = {'id': 7}
        named.fromdict(new, allow_pk=True)
        assert named.asdict() == {'id': new['id'], 'name': named.name}

    def test_simple_aborts_on_named_pk_1(self):
        s = self.session
        named = NamedWithOtherPk('a name')
        s.add(named)
        s.commit()
        new = {'id': 7}
        try:
            named.fromdict(new)
            assert False
        except Exception, e:
            assert True, str(e)

    def test_one_to_many_plain(self):
        child = OneToManyChild('child')
        self.session.add(child)
        parent = OneToManyParent('parent')
        parent.child = child
        self.session.add(parent)
        self.session.commit()

        parent.fromdict({'name': 'Parent new name',\
                'child': {'name': 'Child new name'}}, follow=['child'])
        result = parent.asdict(follow=['child'])
        expected = {'id': parent.id, 'name': 'Parent new name',\
                'child': {'id': child.id, 'name': 'Child new name'}}

        assert result == expected, "%r == %r" % (result, expected)

    def test_include(self):
        h = WithHybrid(1)
        h.fromdict({'id': 17}, include=['id'])
        assert h.id == 17

    def test_default_include(self):
        h = WithDefaultInclude(1)
        h.fromdict({'id_alias': 4})
        assert h.id_alias == 4

