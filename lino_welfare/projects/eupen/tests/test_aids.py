# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.

"""Miscellaneous tests on an empty database.

You can run only these tests by issuing::

  $ cd lino_welfare/projects/eupen
  $ python manage.py test tests.test_aids

"""

from __future__ import unicode_literals
from builtins import str

from django.conf import settings
from django.utils import translation
from django.core.exceptions import ValidationError

from atelier.utils import i2d

from lino.api import rt
from lino.utils.djangotest import TestCase

from lino.modlib.users.choicelists import UserTypes

from lino_welfare.modlib.aids.choicelists import ConfirmationTypes


class TestCase(TestCase):
    """"""
    maxDiff = None

    def test_aids(self):
        """Test whether 

        """
        # print("20180502 test_aids.test_aids()")
        RefundConfirmation = rt.models.aids.RefundConfirmation
        Granting = rt.models.aids.Granting
        AidType = rt.models.aids.AidType
        RefundConfirmations = rt.models.aids.RefundConfirmations
        User = settings.SITE.user_model
        Client = rt.models.pcsw.Client
        ClientContactType = rt.models.clients.ClientContactType

        robin = self.create_obj(
            User, username='robin', user_type=UserTypes.admin)

        cli = self.create_obj(
            Client, first_name="First", last_name="Client")

        pt = self.create_obj(
            ClientContactType, name="Apotheke")

        ct = ConfirmationTypes.get_by_value(
                'aids.RefundConfirmation')
        aid_type = self.create_obj(
            AidType, name="foo", confirmation_type=ct,
            pharmacy_type=pt)
        grant = self.create_obj(
            Granting, client=cli, aid_type=aid_type)

        ar = RefundConfirmations.request(user=robin)
        obj = ar.create_instance(granting=grant)

        self.assertEqual(str(obj), 'foo/22.05.14/100/None')

        grant.start_date = i2d(20180401)
        grant.full_clean()
        grant.save()
        
        obj = ar.create_instance(
            granting=grant,
            start_date=i2d(20180331), end_date=i2d(20180331))
        with translation.override('en'):
            try:
                obj.full_clean()
                self.fail("Expected ValidationError")
            except ValidationError as e:
                self.assertEqual(
                    str(e), "[u'Date range 31/03/2018...31/03/2018 lies outside of granted period 01/04/2018....']")
                

        

