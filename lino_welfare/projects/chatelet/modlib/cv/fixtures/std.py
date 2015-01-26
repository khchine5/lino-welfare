# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Standard fixture for :mod:`lino_modlib.projects.chatelet.modlib.cv`.

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)


from django.utils.translation import ugettext_lazy as _

from lino.modlib.cv.fixtures.std import objects as stdobjects

from lino.api import dd, rt


def objects():
    yield stdobjects()

    def proof(name):
        return rt.modules.cv.Proof(**dd.str2kw('name', name))

    yield proof(_("Declarative"))
    yield proof(_("Certificate"))
    yield proof(_("Attestation"))
    yield proof(_("Diploma"))
