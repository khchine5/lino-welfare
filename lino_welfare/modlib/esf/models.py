# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

"""Defines database models for this plugin.
"""

from __future__ import unicode_literals
from __future__ import print_function

from builtins import str
from django.db import models
from django.conf import settings

from lino.api import rt, dd, _
from lino import mixins
from etgen.html import E
from lino.modlib.summaries.mixins import Summary

from lino_welfare.modlib.integ.roles import IntegrationAgent
from lino_xl.lib.excerpts.mixins import Certifiable
from .choicelists import ParticipationCertificates, StatisticalFields


class ClientSummary(Certifiable, Summary):
    """An **ESF summary** is a database object which represents one "fiche
    stagiaire".

    """

    class Meta:
        verbose_name = _("ESF Summary")
        verbose_name_plural = _("ESF Summaries")

    summary_period = 'yearly'

    master = dd.ForeignKey('pcsw.Client')
    education_level = dd.ForeignKey('cv.EducationLevel', blank=True, null=True)
    children_at_charge = models.BooleanField(
        _("Children at charge"), default=False)
    certified_handicap = models.BooleanField(
        _("Certified handicap"), default=False)
    other_difficulty = models.BooleanField(
        _("Other difficulty"), default=False)
    result = ParticipationCertificates.field(blank=True)
    remark = models.CharField(
        _("Remark"),
        blank=True, max_length=200)

    # @classmethod
    # def get_summary_master_model(cls):
    #     return rt.models.pcsw.Client

    @classmethod
    def get_summary_masters(cls):
        return rt.models.pcsw.Client.objects.filter(has_esf=True)

    def get_summary_collectors(self):
        """Loop over all presences of this client, then over all immersion
        contracts and over all job supplyment contracts.

        """
        qs = rt.models.cal.Guest.objects.all()
        qs = self.add_date_filter(
            qs, 'event__start_date', partner=self.master)
        yield (self.collect_from_guest, qs)

        if dd.is_installed('immersion'):
            qs = rt.models.immersion.Contract.objects.all()
            qs = self.add_date_filter(
                qs, 'applies_from', client=self.master)
            yield (self.collect_from_immersion_contract, qs)

        if dd.is_installed('jobs'):
            qs = rt.models.jobs.Contract.objects.all()
            qs = self.add_date_filter(
                qs, 'applies_from', client=self.master)
            yield (self.collect_from_jobs_contract, qs)

    def reset_summary_data(self):
        for sf in StatisticalFields.objects():
            setattr(self, sf.field_name, sf.field.get_default())

    def add_from_fields(self, obj, meth_name):
        for sf in StatisticalFields.objects():
            meth = getattr(sf, meth_name)
            value = meth(obj, self)
            if value:
                value += getattr(self, sf.field_name)
                setattr(self, sf.field_name, value)

    def collect_from_guest(self, obj):
        self.add_from_fields(obj, 'collect_from_guest')

    def collect_from_immersion_contract(self, obj):
        self.add_from_fields(obj, 'collect_from_immersion_contract')

    def collect_from_jobs_contract(self, obj):
        self.add_from_fields(obj, 'collect_from_jobs_contract')

    @dd.displayfield(_("Results"))
    def results(self, ar):
        if ar is None:
            return
        cells = []
        for sf in StatisticalFields.objects():
            v = getattr(self, sf.field_name)
            cells.append(E.td(
                str(sf.text), E.br(), str(v),
                **ar.renderer.cellattrs))
        return E.table(E.tr(*cells), **ar.renderer.tableattrs)


class Summaries(dd.Table):
    """Base class for all tables on :class:`Summary`.
    """
    model = 'esf.ClientSummary'
    detail_layout = """
    master year month
    children_at_charge certified_handicap other_difficulty id
    education_level result remark
    results
    """
    allow_create = False
    hide_sums = True
    # insert_layout = """
    # master
    # education_level result
    # remark
    # """


class AllSummaries(Summaries):
    """Lists all ESF summaries for all clients."""
    required_roles = dd.login_required(dd.SiteStaff)


class SummariesByClient(Summaries):
    """Lists the ESF summaries for a given client."""
    master_key = 'master'
    auto_fit_column_widths = True
    required_roles = dd.login_required(IntegrationAgent)
    # display_mode = 'html'
    # insert_layout = """
    # education_level result
    # remark
    # """

    @classmethod
    def setup_columns(cls):
        cls.column_names = "year"
        for sf in StatisticalFields.items():
            if sf.field_name is not None:
                cls.column_names += ' ' + sf.field_name
        
dd.inject_field(
    'pcsw.Client', 'has_esf', models.BooleanField(_("ESF data"), default=True))

