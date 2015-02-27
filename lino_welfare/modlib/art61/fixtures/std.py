# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds a default contract type for art61.

"""

from lino.api import dd, rt, _


def objects():
    CT = rt.modules.art61.ContractType
    yield CT(**dd.str2kw('name', _("Default")))