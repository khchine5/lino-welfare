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
Part of :mod:`lino_welfare.modlib.pcsw`.
Defines the :class:`ClientAddress` class,
the :class:`ClientAddressTypes` choicelist.
"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd

contacts = dd.resolve_app('contacts')


class ClientAddressTypes(dd.ChoiceList):
    verbose_name_plural = _("Address type")
add = ClientAddressTypes.add_item
add('01', _("Official address"), 'official')  # IT020
add('02', _("Unverified address"), 'unverified')  # IT042
add('03', _("Declared address"), 'declared')  # IT214
add('10', _("Address on eID card"), 'eid')  # read from eid card


class ClientAddress(contacts.AddressLocation):

    class Meta:
        verbose_name = _("Client Address")
        verbose_name_plural = _("Client Addresses")

    type = ClientAddressTypes.field(
        blank=True, null=True, editable=False)
    client = dd.ForeignKey('pcsw.Client', related_name='addresses_by_client')
    # remark = dd.CharField(_("Remark"), max_length=50, blank=True)

    primary = models.BooleanField(
        _("Primary"),
        default=False,
        help_text=_("""There's at most one primary address per client. \
        Enabling this field will automatically make the other \
        addresses non-primary."""))

    allow_cascaded_delete = ['client']

    def after_ui_save(self, ar):
        super(ClientAddress, self).after_ui_save(ar)
        if self.primary:
            for o in self.client.addresses_by_client.exclude(id=self.id):
                if o.primary:
                    o.primary = False
                    o.save()
            for k in ADDRESS_FIELDS:
                setattr(self.client, k, getattr(self, k))
            self.client.save()
            ar.response.update(refresh_all=True)

ADDRESS_FIELDS = dd.fields_list(
    ClientAddress,
    'street street_no street_box addr1 addr2 zip_code city region country')


class ClientAddresses(dd.Table):
    model = 'pcsw.ClientAddress'
    required = dd.required(user_level='admin')
    detail_layout = dd.FormLayout("""
    type remark
    country city zip_code
    addr1
    street street_no street_box
    addr2
    """, window_size=(60, 'auto'))


class AddressesByClient(ClientAddresses):
    required = dd.required()
    master_key = 'client'
    column_names = 'type:10 remark:10 address_column:30 primary:5'
    label = _("Addresses")
    auto_fit_column_widths = True


__all__ = [
    'ClientAddressTypes',
    'ClientAddress',
    'ClientAddresses',
    'AddressesByClient', 'ADDRESS_FIELDS']
