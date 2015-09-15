# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Some test cases for :mod:`lino_welfare.modlib.debts`.

How to run only this test::

  $ go welfare
  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_debts

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

import os
import json
from bs4 import BeautifulSoup


from lino.utils.djangotest import RemoteAuthTestCase
from lino.utils import AttrDict
from django.utils.datastructures import MultiValueDict

from django.conf import settings
from lino.modlib.users.choicelists import UserProfiles
from lino.api.shell import countries, pcsw, users
from lino.api import rt
from lino.api.doctest import test_client


def readfile(name):
    fn = os.path.join(os.path.dirname(__file__), name)
    return open(fn).read()


class DebtsTests(RemoteAuthTestCase):
    maxDiff = None
    # override_djangosite_settings = dict(use_java=True)

    def test01(self):

        u = users.User(username='root',
                       profile=UserProfiles.admin,
                       language="en")
        u.save()
        # be = countries.Country(name="Belgium", isocode="BE")
        # be.save()
        # kw = dict()
        # # kw.update(card_number="123456789")
        # # kw.update(national_id="680601 053-29")
        # kw.update(id=116)
        # kw.update(first_name="Jean")
        # kw.update(middle_name="Jacques")
        # kw.update(last_name="Jeffin")
        # obj = pcsw.Client(**kw)
        # obj.full_clean()
        # obj.save()

        from lino_welfare.modlib.debts.fixtures.minimal import objects
        for o in objects():
            o.save()
        # from lino.modlib.households.fixtures.std import objects
        # for o in objects():
        #     o.save()

        # Reproduce ticket #521
        ar = rt.login('root')
        # Member = rt.modules.households.Member
        Household = rt.modules.households.Household
        Person = rt.modules.contacts.Person
        Genders = rt.modules.system.Genders
        Budget = rt.modules.debts.Budget
        
        p1 = Person(first_name="A", last_name="A", gender=Genders.male)
        p1.save()
        p2 = Person(first_name="B", last_name="B", gender=Genders.female)
        p2.save()
        h = Household.create_household(ar, p1, p2, None)

        # The household has for whatever reason an empty member
        # entry. Lino should ignore this entry.
        h.add_member(None)

        b = Budget(partner=h, user=u)
        b.save()
        b.fill_defaults()
        # from django.utils.encoding import force_unicode
        # s = ' & '.join([force_unicode(a) for a in b.get_actors()])
        # s = '{0} & {1}'.format(*b.get_actors())
        # self.assertEqual(s, "Mr. & Mrs.")

        # reproduce ticket #159:
        
        self.assertEqual(b.user.username, 'root')
        self.assertEqual(b.id, 1)

        ou = users.User(username='other',
                        profile=UserProfiles.admin,
                        language="en")
        ou.save()
        ar = rt.login('other')
        new = b.duplicate.run_from_code(ar)
        self.assertEqual(new.user.username, 'other')
        self.assertEqual(new.id, 2)
        
        url = "/api/debts/Budgets/1?&pv=&"
        url += "an=duplicate&sr=1"
        res = test_client.get(url, REMOTE_USER='other')
        rv = json.loads(res.content)
        self.assertEqual(
            rv['message'],
            u'Duplicated Budget 1 for A-B to Budget 3 for A-B.')
