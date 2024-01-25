import datetime
import json

import DateTime
from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.memoize.view import memoize
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class TaskInformationView(DefaultView):
    @property
    @memoize
    def year(self):
        current_year = datetime.date.today().year
        return int(self.request.get("year", current_year))

    @property
    @memoize
    def categories(self):
        factory = getUtility(IVocabularyFactory, "collective.taxonomy.task_categories")
        categories = {term.value: term.title for term in factory(None)}
        return categories

    @property
    def task_counts(self):
        category_values = self.categories.keys()
        users = api.user.get_users()
        infos = {}
        for u in users:
            user_infos = {
                "fullname": u.getProperty("fullname"),
                "counts": {c: 0 for c in category_values},
            }
            infos[u.getId()] = user_infos
        start = DateTime.DateTime(self.year - 1, 12, 1)  # 1st December of previous year
        end = DateTime.DateTime(self.year, 12, 1)  # 1st December of current year
        start_query = {"query": (start, end), "range": "min:max"}
        brains = api.content.find(
            context=self.context,
            portal_type="divingclub.Task",
            sort_on="start",
            start=start_query,
        )
        for b in brains:
            task = b.getObject()
            if task.manager in infos and task.category in category_values:
                infos[task.manager]["counts"][task.category] += 1
        # Remove members with 0 tasks
        uids = [uid for uid in infos.keys()]
        for uid in uids:
            total = sum(infos[uid]["counts"].values())
            if total == 0:
                del infos[uid]

        return infos.values()
