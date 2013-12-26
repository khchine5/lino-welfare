# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
.. setting:: cbss.cbss_live_tests

Whether unit tests should try to really connect to the cbss.
Some test cases of the test suite would fail with a timeout if run 
from behind an IP address that is not registered at the :term:`CBSS`.
These tests are skipped by default. To activate them,
set `cbss_live_tests` to `True` in your :xfile:`settings.py`.
    
.. setting:: cbss.cbss_environment

Either `None` or one of 'test', 'acpt' or 'prod'.
See :mod:`lino_welfare.modlib.cbss.models`.
Leaving this to `None` means that the cbss app
is "inactive" even if installed.

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("CBSS")

    cbss_live_tests = False

    #~ cbss_environment = None
    cbss_environment = 'test'

    def __init__(self, *args):
        super(Plugin, self).__init__(*args)
        for k in 'cbss_environment cbss_live_tests'.split():
            if hasattr(self.site, k):
                v = getattr(self.site, k)
                raise Exception("""%s has an attribute '%s'!.
You probably want to replace this by:
SITE.plugins.cbss.configure(%s=%r)
""" % (self.site, k, k, v))
