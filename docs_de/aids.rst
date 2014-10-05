.. _welfare.tested.aids:

============
Beihilfen
============

..
  This document is part of the test suite.
  To test only this document, run::
    $ python setup.py test -s tests.DocsTests.test_aids

..
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
    >>> from bs4 import BeautifulSoup
    >>> from lino.utils import i2d
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.runtime import *
    >>> from django.test import Client
    >>> from django.utils import translation
    >>> import json
    >>> client = Client()




>>> ses = rt.login('rolf')
>>> translation.activate('de')

Die Demo-Datenbank ist datiert auf den 22. Mai 2014:

>>> print(dd.fdl(dd.demo_date()))
22. Mai 2014



Hilfearten
==========

Hier eine Liste der Hilfearten, die Lino kennt:

>>> ses.show(aids.AidTypes, column_names="name confirmed_by_primary_coach body_template")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================================================= =========================== ============================
 Bezeichnung                                       Primärbegleiter bestätigt   Body template
------------------------------------------------- --------------------------- ----------------------------
 Ausländerbeihilfe                                 Ja                          foreigner_income.body.html
 DMH-Übernahmeschein                               Ja                          certificate.body.html
 Eingliederungseinkommen                           Ja                          integ_income.body.html
 Erstattung                                        Ja                          certificate.body.html
 Feste Beihilfe                                    Ja                          fixed_income.body.html
 Heizkosten                                        Ja                          heating_refund.body.html
 Lebensmittelbank                                  Nein                        food_bank.body.html
 Möbellager                                        Ja                          furniture.body.html
 Übernahme von Arzt- und/oder Medikamentenkosten   Ja                          certificate.body.html
 Übernahmeschein                                   Ja                          certificate.body.html
 **Total (10 Zeilen)**                             **9**
================================================= =========================== ============================
<BLANKLINE>



Beschlüsse und Bestätigungen
============================

Lino unterscheidet zwischen Hilfe\ *beschlüssen*
(:class:`Granting <welfare.aids.Granting>`) und Hilfe\ *bestätigungen*
(:class:`Confirmation <welfare.aids.Confirmation>`).

Hilfe\ *bestätigungen* sind "Präzisierungen" eines Hilfe\
*beschlusses*.  Beschlüsse sind *prinzipiell*, *langfristig* und
*allgemein*, Bestätigungen sind *detailliert*, *befristet* und
*konkret*.  Der Beschluss ist sozusagen die Erlaubnis oder Grundlage,
Bestätigungen für eine bestimmte Hilfeart auszuhändigen.

Zum Beispiel ist es ein *Beschluss*, wenn jemand
*Eingliederungseinkommen* erhält.  Aber der monatliche Betrag steht
nicht im *Beschluss*, sondern nur in der *Bestätigung*, weil der sich
im Laufe der Zeit ändern kann.

Oder wenn jemand Anrecht auf *Übernahme von Arzt- und
Medikamentenkosten* hat, ist das ein *Beschluss*. Um daraus eine
*Bescheinigung* zu machen, muss man auch *Apotheke* und *Arzt*
angeben.

Bemerkungen
===========

- Es gibt Hilfearten (z.B. “Erstattung”), für die nie eine
  Bescheinigung gedruckt wird. Deren Feld (:attr:`Bescheinigungsart
  <welfare.aids.AidType.confirmation_type>` ist leer.

- Einen “Bestätiger” (:attr:`signer
  <welfare.aids.Confirmable.signer>`) kann es pro Bescheinigung als
  auch pro Beschluss geben.  Bestätiger des Beschlusses ist par défaut
  der Primärbegleiter, Bestätiger einer Bescheinigung ist der des
  Beschlusses.

- Pro Bescheinigung auch die Apotheke sehen und ändern können (d.h.:
  Neue Felder AidType.pharmacy_type und RefundConfirmation.pharmacy.
  (ist allerdings noch nicht vorbelegt aus Klientenkontakt)




Hilfebeschlüsse
===============

Alicia hat 2 Hilfebestätigungen zu unterschreiben. Dies kriegt sie als
Willkommensmeldung unter die Nase gerieben:

>>> ses = rt.login('alicia')
>>> translation.activate('de')
>>> for msg in settings.SITE.get_welcome_messages(ses):
...     print(E.tostring(msg))
<span>Du bist besch&#228;ftigt mit <b>Collard Charlotte (118)</b>.</span>
<span>Du hast 1 Eintr&#228;ge in <i>Zu unterschreibende Hilfebeschl&#252;sse</i>.</span>


>>> ses.show(aids.MyPendingGrantings)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======================== ===================== ============== ===== ======= ================================
 Klient                   Hilfeart              Laufzeit von   bis   Autor   Arbeitsablauf
------------------------ --------------------- -------------- ----- ------- --------------------------------
 FAYMONVILLE Luc (130*)   DMH-Übernahmeschein   28.05.14                     **Unbestätigt** → [Bestätigen]
======================== ===================== ============== ===== ======= ================================
<BLANKLINE>


Hilfebestätigungen
==================

In der Demo-Datenbank gibt es 2 generierte Bescheinigungen pro Hilfeart :

>>> translation.activate('de')
>>> for at in aids.AidType.objects.exclude(confirmation_type=''):
...    M = at.confirmation_type.model
...    qs = M.objects.filter(granting__aid_type=at)
...    obj = qs[0]
...    txt = obj.confirmation_text()
...    txt = ' '.join(txt.split())
...    print("%s : %d" % (unicode(at), qs.count()))
Eingliederungseinkommen : 2
Ausländerbeihilfe : 2
Feste Beihilfe : 2
Erstattung : 2
Übernahmeschein : 2
Übernahme von Arzt- und/oder Medikamentenkosten : 2
DMH-Übernahmeschein : 2
Möbellager : 2
Heizkosten : 2
Lebensmittelbank : 2

Beispiele
=========


Für die Hilfearten aus obiger Liste, für die eine Vorlage definiert
ist (also für wir nicht bloß den generischen Bestätigungstext haben)
hier die gleichen Texte als HTML:

.. django2rst::

    from __future__ import unicode_literals
    from django.utils import translation
    from atelier.rstgen import header
    ses = rt.login("rolf")
    translation.activate('de')

    for at in aids.AidType.objects.exclude(confirmation_type=''):
        M = at.confirmation_type.model
        qs = M.objects.filter(granting__aid_type=at)
        obj = qs[0]
        ex = obj.printed_by
        if ex:
            print(header(5, unicode(at)))
            print(header(6, "Beispiel"))
            print("")
            print(".. raw:: html")
            print("")
            for ln in ex.preview(ses).splitlines():
                print("    " + ln)
            print("")
    
            print(header(6, "Vorlage"))
            print("::")
            print("")
            for ln in ex.body_template_content(ses).splitlines():
                print("    " + ln)
            print("")

    print("")


