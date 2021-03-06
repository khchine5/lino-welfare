.. _welfare.specs.debts:

===============
Debts mediation
===============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_debts
    
    Doctest initialization:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *

    >>> ses = rt.login('rolf')
    >>> translation.activate('de')
    
The :mod:`lino_welfare.modlib.debts` modules adds functionality for
managing "budgets".     
    
.. contents::
   :local:
   :depth: 1



Budgets
=======
    
A :class:`Budget
<lino_welfare.modlib.debts.modles.Budget>` is a document based on
financial data about a person or household.  It is just about entering
this data and then printing it.

The demo database has 14 such documents with fictive generated data:

>>> debts.Budget.objects.count()
14

For the following examples we will use budget no. 3:

>>> obj = debts.Budget.objects.get(pk=3)
>>> obj
Budget #3 ('Budget Nr. 3 f\xfcr J\xe9r\xf4me & Theresia Jean\xe9mart-Thelen')


Actors
======

This budget has 3 actors:

>>> len(obj.get_actors())
3

Every actor is an instance of :class:`Actor
<lino_welfare.modlib.debts.models.Actor>`, which is designed to be
used in templates. For example, every actor has four attributes
`header`, `person`, `client` and `household`:

>>> u = attrtable(obj.get_actors(), 'header person client household')
>>> print(u)
=========== ======================= ======================== ==========================================================
 header      person                  client                   household
----------- ----------------------- ------------------------ ----------------------------------------------------------
 Gemeinsam   None                    None                     Jérôme & Theresia Jeanémart-Thelen (Faktischer Haushalt)
 Mr.         Herr Jérôme JEANÉMART   JEANÉMART Jérôme (181)   None
 Mrs.        Frau Theresia THELEN    None                     None
=========== ======================= ======================== ==========================================================
<BLANKLINE>


Data entry panels
=================

Here is the textual representation of the "Expenses" panel:

>>> ses.show(debts.ExpensesByBudget, obj,
...   column_names="account description amount remark",
...   limit=10)
... #doctest: +NORMALIZE_WHITESPACE
====================================== ====================== ============ ===========
 Konto                                  Beschreibung           Betrag       Bemerkung
-------------------------------------- ---------------------- ------------ -----------
 (3010) Miete                           Rent                   41,00
 (3011) Wasser                          Water                  47,00
 (3012) Strom                           Electricity
 (3020) Festnetz-Telefon und Internet   Telephone & Internet   5,00
 (3021) Handy                           Cell phone             10,00
 (3030) Fahrtkosten                     Transport costs        15,00        Cinema
 (3030) Fahrtkosten                     Transport costs        15,00        Shopping
 (3031) TEC Busabonnement               Public transport       20,00
 (3032) Benzin                          Fuel                   26,00
 (3033) Unterhalt Auto                  Car maintenance        31,00
 **Total (35 Zeilen)**                                         **210,00**
====================================== ====================== ============ ===========
<BLANKLINE>

Note that the above table contains a mixture of German and English
texts because our **current language** is German while the **partner**
speaks English:

>>> print(obj.partner.language)
<BLANKLINE>

Description and Remark have been entererd for this particular Budget
instance and are therefore in the partner's language. Everything else
depends on the current user language.


The summary panel
=================

Here are some more slave tables.

>>> ses.show(debts.ResultByBudget, obj)
========================================================= ==============
 Beschreibung                                              Betrag
--------------------------------------------------------- --------------
 Monatliche Einkünfte                                      5 000,00
 Monatliche Ausgaben                                       -565,00
 Monatliche Reserve für jährliche Ausgaben (236,00 / 12)   -19,67
 Raten der laufenden Kredite                               -45,00
 **Restbetrag für Kredite und Zahlungsrückstände**         **4 370,33**
========================================================= ==============
<BLANKLINE>

>>> obj.include_yearly_incomes = True
>>> ses.show(debts.ResultByBudget, obj)
========================================================= ==============
 Beschreibung                                              Betrag
--------------------------------------------------------- --------------
 Monatliche Einkünfte                                      5 000,00
 Jährliche Einkünfte (2 400,00 / 12)                       200,00
 Monatliche Ausgaben                                       -565,00
 Monatliche Reserve für jährliche Ausgaben (236,00 / 12)   -19,67
 Raten der laufenden Kredite                               -45,00
 **Restbetrag für Kredite und Zahlungsrückstände**         **4 570,33**
========================================================= ==============
<BLANKLINE>

>>> ses.show(debts.DebtsByBudget, obj)
================================== ==============
 Beschreibung                       Betrag
---------------------------------- --------------
 Kredite                            300,00
 Schulden                           600,00
 Zahlungsrückstände (verteilbar)    900,00
 Gerichtsvollzieher (verteilbar)    1 200,00
 Inkasso-Unternehmen (verteilbar)   1 500,00
 **Verpflichtungen**                **4 500,00**
================================== ==============
<BLANKLINE>

>>> with translation.override('en'):
...     ses.show(debts.DebtsByBudget, obj)
================================= ==============
 Description                       Amount
--------------------------------- --------------
 Loans                             300,00
 Debts                             600,00
 Invoices to pay (distributable)   900,00
 Bailiff (distributable)           1 200,00
 Cash agency (distributable)       1 500,00
 **Liabilities**                   **4 500,00**
================================= ==============
<BLANKLINE>

>>> ses.show(debts.DistByBudget, obj, language="en")
==================== ================= ============== ============ ===========================
 Creditor             Description       Debt           %            Monthly payback suggested
-------------------- ----------------- -------------- ------------ ---------------------------
 Auto École Verte     Invoices to pay   900,00         25,00        30,00
 ÖSHZ Kettenis        Bailiff           1 200,00       33,33        40,00
 BISA                 Cash agency       1 500,00       41,67        50,00
 **Total (3 rows)**                     **3 600,00**   **100,00**   **120,00**
==================== ================= ============== ============ ===========================
<BLANKLINE>

The printed document
====================

The following table shows how Lino renders remarks in the printed
version: they are added to the description between parentheses
(e.g. "Spare time"), and if several entries were grouped into a same
printable row (e.g. "Fahrtkosten"), they are separated by commas.

>>> groups = list(obj.entry_groups(ses))
>>> with translation.override('en'):
...     ses.show(groups[0].action_request)
... #doctest: -REPORT_UDIFF
==================== ========= ======== ===== ============== ==============
 Description          Remarks   Common   Mr.   Mrs.           Total
-------------------- --------- -------- ----- -------------- --------------
 Salaries                                      800,00         800,00
 Pension                                       1 000,00       1 000,00
 Integration aid                               1 200,00       1 200,00
 Ersatzeinkünfte                               1 400,00       1 400,00
 Aliments
 Chèques-repas                                 200,00         200,00
 Andere                                        400,00         400,00
 **Total (7 rows)**                            **5 000,00**   **5 000,00**
==================== ========= ======== ===== ============== ==============
<BLANKLINE>

>>> with translation.override('en'):
...     ses.show(groups[1].action_request)
... #doctest: +REPORT_UDIFF
====================== ================== =============== ============ ===== ====== ============
 Description            Remarks            Yearly amount   Common       Mr.   Mrs.   Total
---------------------- ------------------ --------------- ------------ ----- ------ ------------
 Rent                                      492,00          41,00                     41,00
 Water                                     564,00          47,00                     47,00
 Electricity
 Telephone & Internet                      60,00           5,00                      5,00
 Cell phone                                120,00          10,00                     10,00
 Transport costs        Cinema, Shopping   360,00          30,00                     30,00
 Public transport                          240,00          20,00                     20,00
 Fuel                                      312,00          26,00                     26,00
 Car maintenance                           372,00          31,00                     31,00
 School                                    432,00          36,00                     36,00
 Babysitting                               492,00          41,00                     41,00
 Health                                    564,00          47,00                     47,00
 Clothes
 Food                                      60,00           5,00                      5,00
 Hygiene                                   120,00          10,00                     10,00
 Health insurance                          180,00          15,00                     15,00
 Labour fees                               240,00          20,00                     20,00
 Unterhaltszahlungen                       312,00          26,00                     26,00
 Retirement savings                        372,00          31,00                     31,00
 Tobacco                                   432,00          36,00                     36,00
 Spare time             Seminar            492,00          41,00                     41,00
 Pets                                      564,00          47,00                     47,00
 Other
 **Total (23 rows)**                       **6 780,00**    **565,00**                **565,00**
====================== ================== =============== ============ ===== ====== ============
<BLANKLINE>


>>> with translation.override('en'):
...     ses.show(groups[2].action_request)
... #doctest: +REPORT_UDIFF
==================================== ======== ===== ============ ============
 Description                          Common   Mr.   Mrs.         Total
------------------------------------ -------- ----- ------------ ------------
 Paid holiday (600.00 / 12)                          50,00        50,00
 Year-end prime (800.00 / 12)                        66,67        66,67
 Gewerkschaftsprämie (1000.00 / 12)                  83,33        83,33
 **Total (3 rows)**                                  **200,00**   **200,00**
==================================== ======== ===== ============ ============
<BLANKLINE>



Something in French
===================

>>> with translation.override('fr'):
...    ses.show(debts.DistByBudget, obj)
====================== ================= ============== ============ =======================
 Créancier              Description       Dette          %            Remboursement mensuel
---------------------- ----------------- -------------- ------------ -----------------------
 Auto École Verte       Invoices to pay   900,00         25,00        30,00
 ÖSHZ Kettenis          Bailiff           1 200,00       33,33        40,00
 BISA                   Cash agency       1 500,00       41,67        50,00
 **Total (3 lignes)**                     **3 600,00**   **100,00**   **120,00**
====================== ================= ============== ============ =======================
<BLANKLINE>

Or the same in English:

>>> with translation.override('en'):
...     ses.show(debts.DistByBudget, obj)
==================== ================= ============== ============ ===========================
 Creditor             Description       Debt           %            Monthly payback suggested
-------------------- ----------------- -------------- ------------ ---------------------------
 Auto École Verte     Invoices to pay   900,00         25,00        30,00
 ÖSHZ Kettenis        Bailiff           1 200,00       33,33        40,00
 BISA                 Cash agency       1 500,00       41,67        50,00
 **Total (3 rows)**                     **3 600,00**   **100,00**   **120,00**
==================== ================= ============== ============ ===========================
<BLANKLINE>

Note that the Description still shows German words because these are stored per Budget, 
and Budget #3 is addressed to a German-speaking partner.


A web request
=============

The following snippet reproduces a one-day bug 
discovered :blogref:`20130527`:

>>> url = '/api/debts/Budgets/3?fmt=json&an=detail'
>>> test_client.force_login(rt.login('rolf').user)
>>> res = test_client.get(url,REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(' '.join(sorted(result.keys())))
data disable_delete id navinfo title


Editability of tables
=====================

The following is to check whether the editable attribute inherited 
correctly.

>>> debts.Budgets.editable
True
>>> debts.EntriesByBudget.editable
True
>>> debts.DistByBudget.editable
False
>>> debts.LiabilitiesByBudget.editable
True
>>> debts.PrintEntriesByBudget.editable
False



The first meeting of a budget
=============================

>>> translation.activate('en')
    
The following shows how we use the
:meth:`lino_welfare.modlib.debts.models.Actor.get_first_meeting`
method for printing the date and user of the first meeting.

Here is a list of all actors for which there is a first meeting.

>>> msg = "Budget {0} : First meeting on {1} with user {2}"
>>> for actor in debts.Actor.objects.all():
...     n = actor.get_first_meeting()
...     if n is not None:
...         print(msg.format(actor.budget.id, dd.fdl(n.date), n.user))
Budget 4 : First meeting on 22 July 2013 with user Kerstin Kerres

The `syntax of appy.pod templates
<http://appyframework.org/podWritingTemplates.html>`_ does not yet
have a ``with`` statement.

The :xfile:`Default.odt` template uses this in a construct similar to
the following snippet:

>>> budget = debts.Budget.objects.get(pk=4)
>>> for actor in budget.get_actors():
...     print(actor.get_first_meeting_text())
None
First meeting on 22 July 2013 with Kerstin Kerres
None


The stories
===========

Here is now (almost) the whole content of a printed budget.

>>> obj = debts.Budget.objects.get(pk=4)

>>> ses.story2rst(obj.data_story(ses))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
~~~~~~~~~~~~~~~
Monthly incomes
~~~~~~~~~~~~~~~
<BLANKLINE>
==================== ========= ======== ===== ============== ==============
 Description          Remarks   Common   Mr.   Mrs.           Total
-------------------- --------- -------- ----- -------------- --------------
 Salaries                                      1 200,00       1 200,00
 Pension                                       1 400,00       1 400,00
 Integration aid
 Ersatzeinkünfte                               200,00         200,00
 Aliments                                      400,00         400,00
 Chèques-repas                                 600,00         600,00
 Andere                                        800,00         800,00
 **Total (7 rows)**                            **4 600,00**   **4 600,00**
==================== ========= ======== ===== ============== ==============
<BLANKLINE>
~~~~~~~~~~~~~~~~
Monthly expenses
~~~~~~~~~~~~~~~~
<BLANKLINE>
====================== ================== =============== ============ ===== ====== ============
 Description            Remarks            Yearly amount   Common       Mr.   Mrs.   Total
---------------------- ------------------ --------------- ------------ ----- ------ ------------
 Rent                                      120,00          10,00                     10,00
 Water                                     180,00          15,00                     15,00
 Electricity                               240,00          20,00                     20,00
 Telephone & Internet                      312,00          26,00                     26,00
 Cell phone                                372,00          31,00                     31,00
 Transport costs        Shopping, Cinema   864,00          72,00                     72,00
 Public transport                          492,00          41,00                     41,00
 Fuel                                      564,00          47,00                     47,00
 Car maintenance
 School                                    60,00           5,00                      5,00
 Babysitting                               120,00          10,00                     10,00
 Health                                    180,00          15,00                     15,00
 Clothes                                   240,00          20,00                     20,00
 Food                                      312,00          26,00                     26,00
 Hygiene                                   372,00          31,00                     31,00
 Health insurance                          432,00          36,00                     36,00
 Labour fees                               492,00          41,00                     41,00
 Unterhaltszahlungen                       564,00          47,00                     47,00
 Retirement savings
 Tobacco                                   60,00           5,00                      5,00
 Spare time             Cinema             120,00          10,00                     10,00
 Pets                                      180,00          15,00                     15,00
 Other                                     240,00          20,00                     20,00
 **Total (23 rows)**                       **6 516,00**    **543,00**                **543,00**
====================== ================== =============== ============ ===== ====== ============
<BLANKLINE>
~~~~~~~~~~~~~~
Yearly incomes
~~~~~~~~~~~~~~
<BLANKLINE>
==================================== ======== ===== ============ ============
 Description                          Common   Mr.   Mrs.         Total
------------------------------------ -------- ----- ------------ ------------
 Paid holiday (1000.00 / 12)                         83,33        83,33
 Year-end prime (1200.00 / 12)                       100,00       100,00
 Gewerkschaftsprämie (1400.00 / 12)                  116,67       116,67
 **Total (3 rows)**                                  **300,00**   **300,00**
==================================== ======== ===== ============ ============
~~~~~
Taxes
~~~~~
<BLANKLINE>
===================== ========= =============== =========== ===== ====== ===========
 Description           Remarks   Yearly amount   Common      Mr.   Mrs.   Total
--------------------- --------- --------------- ----------- ----- ------ -----------
 Municipal tax                   26,00           2,17                     2,17
 Kanalisationssteuer             31,00           2,58                     2,58
 Waste tax                       36,00           3,00                     3,00
 Autosteuer                      41,00           3,42                     3,42
 Immobiliensteuer                47,00           3,92                     3,92
 Other
 **Total (6 rows)**              **181,00**      **15,08**                **15,08**
===================== ========= =============== =========== ===== ====== ===========
<BLANKLINE>
~~~~~~~~~~
Insurances
~~~~~~~~~~
<BLANKLINE>
===================== ========= =============== ========== ===== ====== ==========
 Description           Remarks   Yearly amount   Common     Mr.   Mrs.   Total
--------------------- --------- --------------- ---------- ----- ------ ----------
 Fire                            5,00            0,42                    0,42
 Familienhaftpflicht             10,00           0,83                    0,83
 Car insurance                   15,00           1,25                    1,25
 Life insurance                  20,00           1,67                    1,67
 Other insurances                26,00           2,17                    2,17
 **Total (5 rows)**              **76,00**       **6,33**                **6,33**
===================== ========= =============== ========== ===== ====== ==========
<BLANKLINE>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Debts, outsanding payments and credits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<BLANKLINE>
==================== ========= ============== ============ ===== ====== ============
 Partner              Remarks   Monthly rate   Common       Mr.   Mrs.   Total
-------------------- --------- -------------- ------------ ----- ------ ------------
 Pro Aktiv V.o.G.                              900,00                    900,00
 **Total (1 rows)**                            **900,00**                **900,00**
==================== ========= ============== ============ ===== ====== ============
<BLANKLINE>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Bailiffs and cash collectors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<BLANKLINE>
======================== ========================== ========= ============== ======== ============== ============== ==============
 Debt collection agency   Partner                    Remarks   Monthly rate   Common   Mr.            Mrs.           Total
------------------------ -------------------------- --------- -------------- -------- -------------- -------------- --------------
 Cashback sprl            Werkstatt Cardijn V.o.G.                                     1 200,00                      1 200,00
 Money Wizard AS          Behindertenstätten Eupen                                                    1 500,00       1 500,00
 **Total (2 rows)**                                                                    **1 200,00**   **1 500,00**   **2 700,00**
======================== ========================== ========= ============== ======== ============== ============== ==============
<BLANKLINE>


>>> ses.story2rst(obj.summary_story(ses))
... #doctest: +NORMALIZE_WHITESPACE -REPORT_UDIFF
------------------
Incomes & Expenses
------------------
<BLANKLINE>
=================================================== ==============
 Description                                         Amount
--------------------------------------------------- --------------
 Monthly incomes                                     4 600,00
 Monthly expenses                                    -543,00
 Monthly reserve for yearly expenses (257,00 / 12)   -21,42
 **Remaining for credits and debts**                 **4 035,58**
=================================================== ==============
<BLANKLINE>
-----------
Liabilities
-----------
<BLANKLINE>
================================= ==============
 Description                       Amount
--------------------------------- --------------
 Invoices to pay (distributable)   900,00
 Bailiff (distributable)           1 200,00
 Cash agency (distributable)       1 500,00
 **Liabilities**                   **3 600,00**
================================= ==============
<BLANKLINE>
------------------
Debts distribution
------------------
<BLANKLINE>
========================== ================= ============== ============ ===========================
 Creditor                   Description       Debt           %            Monthly payback suggested
-------------------------- ----------------- -------------- ------------ ---------------------------
 Pro Aktiv V.o.G.           Invoices to pay   900,00         25,00        30,00
 Werkstatt Cardijn V.o.G.   Bailiff           1 200,00       33,33        40,00
 Behindertenstätten Eupen   Cash agency       1 500,00       41,67        50,00
 **Total (3 rows)**                           **3 600,00**   **100,00**   **120,00**
========================== ================= ============== ============ ===========================
<BLANKLINE>


Filtering budgets
=================

The :menuselection:`Explorer --> Debt mediation --> Budgets` nenu
command shows the table of all budgets.

>>> kwargs = dict(column_names="id user date partner dist_amount")
>>> ses.show(debts.Budgets, **kwargs)
==== ================== ============ ================================================= ======================
 ID   Author             Date         Partner                                           Distributable amount
---- ------------------ ------------ ------------------------------------------------- ----------------------
 1    Kerstin Kerres     22/05/2014   Gerd & Tatjana Gerkens-Kasennova                  120,00
 2    Patrick Paraneau   22/05/2014   Hubert & Judith Huppertz-Jousten                  120,00
 3    Romain Raffault    22/05/2014   Jérôme & Theresia Jeanémart-Thelen                120,00
 4    Rolf Rompen        22/05/2014   Denis & Mélanie Denon-Mélard                      120,00
 5    Robin Rood         22/05/2014   Robin & Lisa Dubois-Lahm                          120,00
 6    Kerstin Kerres     22/05/2014   Jérôme & Marie-Louise Jeanémart-Vandenmeulenbos   120,00
 7    Patrick Paraneau   22/05/2014   Hubert & Gaby Frisch-Frogemuth                    120,00
 8    Romain Raffault    22/05/2014   Paul & Paula Frisch-Einzig                        120,00
 9    Rolf Rompen        22/05/2014   Paul & Petra Frisch-Zweith                        120,00
 10   Robin Rood         22/05/2014   Ludwig & Laura Frisch-Loslever                    120,00
 11   Kerstin Kerres     22/05/2014   Albert & Eveline Adam-Evrard                      120,00
 12   Patrick Paraneau   22/05/2014   Albert & Françoise Adam-Freisen                   120,00
 13   Romain Raffault    22/05/2014   Bruno & Eveline Braun-Evrard                      120,00
 14   Rolf Rompen        22/05/2014   Bruno & Françoise Braun-Freisen                   120,00
                                                                                        **1 680,00**
==== ================== ============ ================================================= ======================
<BLANKLINE>


The nenu command :menuselection:`Debts mediation --> My budgets` shows
the budgets authored by the requesting user.


>>> ses.show(debts.MyBudgets, **kwargs)
==== ============= ============ ================================= ======================
 ID   Author        Date         Partner                           Distributable amount
---- ------------- ------------ --------------------------------- ----------------------
 4    Rolf Rompen   22/05/2014   Denis & Mélanie Denon-Mélard      120,00
 9    Rolf Rompen   22/05/2014   Paul & Petra Frisch-Zweith        120,00
 14   Rolf Rompen   22/05/2014   Bruno & Françoise Braun-Freisen   120,00
                                                                   **360,00**
==== ============= ============ ================================= ======================
<BLANKLINE>


In order to see the budgets issued by other users, users can manually
select that other user in the filter parameter "Author".

>>> pv = dict(user=users.User.objects.get(username='kerstin'))
>>> kwargs.update(param_values=pv)
>>> ses.show(debts.Budgets, **kwargs)
==== ================ ============ ================================================= ======================
 ID   Author           Date         Partner                                           Distributable amount
---- ---------------- ------------ ------------------------------------------------- ----------------------
 1    Kerstin Kerres   22/05/2014   Gerd & Tatjana Gerkens-Kasennova                  120,00
 6    Kerstin Kerres   22/05/2014   Jérôme & Marie-Louise Jeanémart-Vandenmeulenbos   120,00
 11   Kerstin Kerres   22/05/2014   Albert & Eveline Adam-Evrard                      120,00
                                                                                      **360,00**
==== ================ ============ ================================================= ======================
<BLANKLINE>
