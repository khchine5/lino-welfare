# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
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
Dummy module to satisfy `lino.modlib.courses` dependency
on a ``sales`` app.
"""

from __future__ import unicode_literals
from __future__ import print_function

from lino import dd


class CreateInvoice(dd.Dummy):
    pass


class Invoiceable(dd.Dummy):
    pass


class InvoicingsByInvoiceable(dd.Dummy):
    pass