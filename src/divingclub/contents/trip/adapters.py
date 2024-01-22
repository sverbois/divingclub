from borg.localrole.interfaces import ILocalRoleProvider
from zope.component import adapter
from zope.interface import implementer

from .content import ITrip


@adapter(ITrip)
@implementer(ILocalRoleProvider)
class LocalRoleAdapter(object):
    def __init__(self, context):
        self.context = context

    def getRoles(self, principal):
        """Grant permission for principal"""
        roles = []
        if principal == self.context.manager:
            roles.append("Owner")
            roles.append("Reviewer")
        return roles

    def getAllRoles(self):
        """Grant permissions"""
        return [(self.context.manager, ("Owner", "Reviewer"))]
