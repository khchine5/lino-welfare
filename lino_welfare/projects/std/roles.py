"""
Importing this module defines default user profiles and shortcuts
for :ref:`welfare`.
"""


from lino.core.roles import Anonymous, SiteAdmin
from lino.modlib.office.roles import OfficeOperator
from lino_welfare.modlib.pcsw.roles import SocialAgent
from lino_welfare.modlib.pcsw.roles import SocialStaff
from lino_welfare.modlib.integ.roles import IntegrationAgent
from lino_welfare.modlib.integ.roles import IntegrationStaff
from lino_welfare.modlib.debts.roles import DebtsUser, DebtsStaff
from lino_welfare.modlib.newcomers.roles import NewcomersAgent


class SiteAdmin(
        SiteAdmin,
        IntegrationStaff,
        DebtsStaff,
        NewcomersAgent,
        OfficeOperator):
    """The site adminstrator has permission for everything."""


from lino.modlib.users.choicelists import UserProfiles
from lino.api import _

UserProfiles.clear()

add = UserProfiles.add_item

add('000', _("Anonymous"), Anonymous, name='anonymous',
    readonly=True, authenticated=False)
add('100', _("Integration Agent"),           IntegrationAgent)
add('110', _("Integration Agent (Manager)"), IntegrationStaff)
add('200', _("Newcomers consultant"),        NewcomersAgent)
add('210', _("Reception clerk"),             OfficeOperator)
add('300', _("Debts consultant"),            DebtsUser)
add('400', _("Social agent"),                SocialAgent)
add('410', _("Social agent (Manager)"),      SocialStaff)
add('900', _("Administrator"),               SiteAdmin, name='admin')