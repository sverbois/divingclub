import datetime
import json

from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.memoize.view import memoize
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class MemberInformationView(DefaultView):
    @property
    @memoize
    def categories(self):
        factory = getUtility(IVocabularyFactory, "divingclub.DiverCategories")
        infos = {term.value: term.title for term in factory(None)}
        return infos

    @property
    def member_information(self):
        categories = self.categories
        users = api.user.get_users()
        infos = []
        for u in users:
            user_infos = {
                "lastname": u.getProperty("lastname"),
                "firstname": u.getProperty("firstname"),
                "email": u.getProperty("email"),
                "phone": u.getProperty("phone"),
                "diver_category": categories.get(u.getProperty("diver_category"), None),
                "address": f'{u.getProperty("address_street")} - {u.getProperty("address_postalcode")} {u.getProperty("address_city")}'
            }
            infos.append(user_infos)

        return infos
