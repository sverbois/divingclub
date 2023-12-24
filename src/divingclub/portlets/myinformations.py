from DateTime import DateTime
from plone import api
from Products.Five.browser import BrowserView

from divingclub.vocabularies import get_title_from_vocabulary_value


class PortletView(BrowserView):
    @property
    def informations(self):
        user = api.user.get_current()
        certificate = get_title_from_vocabulary_value(
            "divingclub.DiverCategories",
            user.getProperty("diver_category"),
        )
        infos = {
            "fullname": user.getProperty("fullname"),
            "email": user.getProperty("email"),
            "birthdate": user.getProperty("birthdate"),
            "phone": user.getProperty("phone"),
            "certificate": certificate,
        }
        return infos
