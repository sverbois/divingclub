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
        return {
            "bar_tuesday": "Bar (mardi)",
            "bar_friday": "Bar (vendredi)",
            "inflation": "Gonflage",
            "pool": "Surveillance piscine",
        }

    @property
    def task_counts(self):
        users = api.user.get_users()
        infos = {}
        for u in users:
            user_infos = {
                "fullname": u.getProperty("fullname"),
                "counts": dict.fromkeys(self.categories.keys(), 0),
            }
            infos[u.getId()] = user_infos
        start = DateTime.DateTime(self.year - 1, 12, 1)  # 1st December of previous year
        end = DateTime.DateTime(self.year, 12, 1)  # 1st December of current year
        start_query = {"query": (start, end), "range": "min:max"}
        brains = api.content.find(
            context=self.context,
            portal_type="divingclub.Task",
            sort_on="start",
            review_state="performed",
            start=start_query,
        )
        for b in brains:
            task = b.getObject()
            if task.manager in infos and task.category in ["bar", "inflation", "pool"]:
                if task.category == "bar":
                    if task.start.weekday() == 4:
                        infos[task.manager]["counts"]["bar_friday"] += 1
                    else:
                        infos[task.manager]["counts"]["bar_tuesday"] += 1
                else:
                    infos[task.manager]["counts"][task.category] += 1

        # Remove members with 0 tasks
        uids = [uid for uid in infos.keys()]
        for uid in uids:
            total = sum(infos[uid]["counts"].values())
            if total == 0:
                del infos[uid]

        # Compute discount
        POINT_VALUE = 1.5
        for uid in infos:
            infos[uid]["discount"] = 0.0
            for category in self.categories:
                points = 3 if category == "bar_friday" else 2
                infos[uid]["discount"] += infos[uid]["counts"][category] * points * POINT_VALUE
        return infos.values()
