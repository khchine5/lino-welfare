.. _welfare.specs.courses2:

================
Internal courses
================

.. to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_courses2
    
    doctest init:
    
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.chatelet.settings.doctests'
    >>> from lino.api.doctest import *


.. contents:: 
    :local:
    :depth: 1



This is about *internal* courses
(:mod:`lino_welfare.projects.chatelet.modlib.courses.models`), not
:doc:`courses`.

>>> rt.modules.courses.__name__
'lino_welfare.projects.chatelet.modlib.courses.models'


>>> rt.show(courses.Courses)
============ ======================= ============================ ============= ======= ===============
 Date début   Inscriptions jusqu'au   Workshop series              Instructeur   Local   État
------------ ----------------------- ---------------------------- ------------- ------- ---------------
 12/05/2014   12/05/2014              Cuisine                                            **Brouillon**
 12/05/2014   12/05/2014              Creativity                                         **Brouillon**
 12/05/2014   12/05/2014              Notre premier bébé                                 **Brouillon**
 12/05/2014   12/05/2014              Mathématiques                                      **Brouillon**
 12/05/2014   12/05/2014              Français                                           **Brouillon**
 12/05/2014   12/05/2014              Get active!                                        **Brouillon**
 03/11/2013   03/11/2013              Psycho-social intervention                         **Brouillon**
============ ======================= ============================ ============= ======= ===============
<BLANKLINE>



>>> rt.modules.courses.Courses.params_layout.main
u'topic line teacher user state active:10'

>>> demo_get('robin', 'choices/courses/Courses/topic', 'count rows', 0)
>>> demo_get('robin', 'choices/courses/Courses/teacher', 'count rows', 102)
>>> demo_get('robin', 'choices/courses/Courses/user', 'count rows', 10)


Yes, the demo database has no topics defined:

>>> rt.show(courses.Topics)
No data to display

