# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division

# vim: set fileencoding=utf-8 :
from __future__ import absolute_import, division
from iteralchemy.tests import TestCase, Named, NamedWithOtherPk,\
        NamedOtherColumnName,\
        NamedWithSynonym, OneToManyChild, OneToManyParent,\
        M2mLeft, M2mRight,\
        MultipleChildParent, MultipleChildChild1, MultipleChildChild2,\
        MultipleChildChild1Child


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

    def test_simple_aborts_on_named_pk_1(self):
        s = self.session
        named = NamedWithOtherPk('a name')
        s.add(named)
        s.commit()
        new = {'id': 7}
        try:
            named.fromdict(new)
        except Exception, e:
            print 'Failed as it should', e
        else:
            assert False
