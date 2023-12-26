from DateTime import DateTime
from plone import api
from Products.Five.browser import BrowserView

from divingclub.vocabularies import get_title_from_vocabulary_value


class PortletView(BrowserView):
    @property
    def informations(self):
        user = api.user.get_current()
        diver_category = get_title_from_vocabulary_value(
            "divingclub.DiverCategories",
            user.getProperty("diver_category"),
        )
        infos = {
            "lastname": user.getProperty("lastname"),
            "firstname": user.getProperty("firstname"),
            "email": user.getProperty("email"),
            "birthdate": user.getProperty("birthdate"),
            "phone": user.getProperty("phone"),
            "diver_category": diver_category,
            "address": f'{user.getProperty("address_street")} - {user.getProperty("address_postalcode")} {user.getProperty("address_city")}',
        }
        return infos
