from DateTime import DateTime
from plone import api
from Products.Five.browser import BrowserView


class PortletView(BrowserView):
    @property
    def informations(self):
        user = api.user.get_current()
        infos = {
            "fullname": user.getProperty("fullname"),
            "email": user.getProperty("email"),
            "birthdate": user.getProperty("birthdate"),
            "phone": user.getProperty("phone"),
            "certificate": user.getProperty("certificate"),
        }
        return infos
