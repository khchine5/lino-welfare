# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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
"""Loops through all partners and calls their
:meth:`update_dupable_words
<lino.mixins.dupable.Dupable.update_dupable_words>` method.

"""

from lino.api import rt


def objects():

    for o in rt.models.pcsw.Client.objects.all():
        o.update_dupable_words()

    return []
