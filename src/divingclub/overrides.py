from plone.app.portlets.interfaces import IDefaultDashboard
from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser
from zope.component import adapter
from zope.interface import implementer


@implementer(IDefaultDashboard)
@adapter(IPropertiedUser)
class DefaultDashboardOverride:
    """The default dashboard override."""

    def __init__(self, principal):
        self.principal = principal

    def __call__(self):
        return {
            "plone.dashboard1": (),
            "plone.dashboard2": (),
            "plone.dashboard3": (),
            "plone.dashboard4": (),
        }
