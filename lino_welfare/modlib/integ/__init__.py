# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Provides data definitions used by the Integration Service.


.. autosummary::
   :toctree:

   models
   fixtures.demo



"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Integration")

    def setup_reports_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        #~ m.add_action(site.modules.jobs.OldJobsOverview)
        m.add_action(site.modules.integ.UsersWithClients)

        m.add_action('jobs.JobsOverview')
        m.add_action('integ.ActivityReport')

    def setup_main_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('integ.Clients')
        m.add_action('isip.MyContracts')

        m.add_action('jobs.MyContracts')
        m.add_action('jobs.JobProviders')
        m.add_action('jobs.Jobs')
        m.add_action('jobs.Offers')

    def setup_config_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('isip.ContractTypes')
        m.add_action('isip.ContractEndings')
        m.add_action('isip.ExamPolicies')

        m.add_action('jobs.ContractTypes')
        m.add_action('jobs.JobTypes')
        m.add_action('jobs.Schedules')

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('isip.Contracts')
        m.add_action('jobs.Contracts')
        m.add_action('jobs.Candidatures')
        m.add_action('isip.ContractPartners')
