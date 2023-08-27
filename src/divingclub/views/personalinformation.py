from plone import api
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.base import PloneMessageFactory as _
from z3c.form import button


class OverridedUserDataPanel(UserDataPanel):
    @property
    def redirect_url(self):
        url_portal = api.portal.get().absolute_url()
        return url_portal + "/@@dashboard"

    @button.buttonAndHandler(_("Save"))
    def handleSave(self, action):
        super().handleSave(self, action)
        self.request.response.redirect(self.redirect_url)

    @button.buttonAndHandler(_("Cancel"))
    def cancel(self, action):
        super().cancel(self, action)
        self.request.response.redirect(self.redirect_url)
