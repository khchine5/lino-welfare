# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino Welfare project.
# Lino Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Welfare; if not, see <http://www.gnu.org/licenses/>.

"""
The `models` module for :mod:`lino_welfare.modlib.users`.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from lino import dd

from lino.modlib.users.models import *

cal = dd.resolve_app('cal')


class UserDetail(UserDetail, cal.UserDetailMixin):

    main = "general cal coaching"

    general = dd.Panel("""
    box1:40 MembershipsByUser:20
    remarks:40 AuthoritiesGiven:20
    """, label=_("General"))

    coaching_a = """
    newcomer_quota
    coaching_type
    coaching_supervisor
    newcomers.CompetencesByUser
    """

    coaching = dd.Panel("""
    coaching_a:20 pcsw.CoachingsByUser:40
    """, label=_("Coaching"))


def site_setup(site):
    site.modules.users.Users.set_detail_layout(UserDetail())