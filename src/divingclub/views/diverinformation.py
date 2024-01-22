import datetime
import json

from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.memoize.view import memoize
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class DiverInformationView(DefaultView):
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
                "lifras": u.getProperty("lifras_id"),
                "febras": u.getProperty("febras_id"),
                "category": categories.get(u.getProperty("diver_category"), None),
                "child": "CHILD" if u.getProperty("child_supervisor") else "",
                "nitrox": "NITROX"
                if u.getProperty("nitrox_diver") and not u.getProperty("advanced_nitrox_diver")
                else "",
                "advanced": "NITROX+" if u.getProperty("advanced_nitrox_diver") else "",
            }
            infos.append(user_infos)

        return infos
