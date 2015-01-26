# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for :mod:`lino_modlib.projects.chatelet.modlib.cv`.

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from lino.modlib.cv.models import *


LanguageKnowledgesByPerson.column_names = "language native spoken \
written spoken_passively written_passively *"


class Proof(mixins.BabelNamed):
    class Meta:
        verbose_name = _("Skill proof")
        verbose_name_plural = _("Skill proofs")


class Proofs(dd.Table):
    model = 'cv.Proof'



class PersonProperty(dd.Model):

    allow_cascaded_delete = ['person']

    class Meta:
        abstract = True

    person = models.ForeignKey(config.person_model)
    remark = models.CharField(max_length=200,
                              blank=True,  # null=True,
                              verbose_name=_("Remark"))


class PropsByPerson(dd.Table):
    master_key = 'person'
    auto_fit_column_widths = True


##
## SKILLS
##

class Skill(PersonProperty, SectorFunction):

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

    proof = dd.ForeignKey('cv.Proof', blank=True, null=True)

dd.update_field(Skill, 'remark', verbose_name=_("Competences"))


class Skills(dd.Table):
    model = 'cv.Skill'


class SkillsByPerson(PropsByPerson, Skills):
    column_names = 'sector function remark'


##
## SOFTSKILLS
##


class SoftSkillType(mixins.BabelNamed):
    class Meta:
        verbose_name = _("Soft skill type")
        verbose_name_plural = _("Soft skill types")


class SoftSkillTypes(dd.Table):
    model = 'cv.SoftSkillType'

    
class SoftSkill(PersonProperty):
    class Meta:
        verbose_name = _("Soft skill")
        verbose_name_plural = _("Soft skills")
    type = dd.ForeignKey('cv.SoftSkillType', verbose_name=_("Type"))
    proof = dd.ForeignKey('cv.Proof', blank=True, null=True)


class SoftSkills(dd.Table):
    model = 'cv.SoftSkill'


class SoftSkillsByPerson(PropsByPerson, SoftSkills):
    column_names = 'type remark'

##
## OBSTACLES
##


class ObstacleType(mixins.BabelNamed):
    class Meta:
        verbose_name = _("Obstacle type")
        verbose_name_plural = _("Obstacle types")


class ObstacleTypes(dd.Table):
    model = 'cv.ObstacleType'


class Obstacle(PersonProperty):
    class Meta:
        verbose_name = _("Obstacle")
        verbose_name_plural = _("Obstacles")
    type = dd.ForeignKey('cv.ObstacleType', verbose_name=_("Type"))
    user = dd.ForeignKey(
        'users.User',
        related_name='obstacles_detected',
        verbose_name=_("Detected by"),
        blank=True, null=True)


class Obstacles(dd.Table):
    model = 'cv.Obstacle'


class ObstaclesByPerson(PropsByPerson, Obstacles):
    column_names = 'type user remark'


dd.inject_field('system.SiteConfig', 'propgroup_skills', dd.DummyField())
dd.inject_field('system.SiteConfig', 'propgroup_softskills', dd.DummyField())
dd.inject_field('system.SiteConfig', 'propgroup_obstacles', dd.DummyField())


