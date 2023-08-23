from DateTime import DateTime
from plone import api
from Products.Five.browser import BrowserView


class PortletView(BrowserView):
    @property
    def items(self):
        user_id = api.user.get_current().getId()
        brains = api.content.find(
            portal_type="divingclub.Task",
            start={"query": DateTime(), "range": "min"},
            sort_on="start",
        )
        infos = []
        for b in brains:
            task = b.getObject()
            if task.manager == user_id:
                info = {
                    "category_title": task.category_title,
                    "start": task.start,
                    "end": task.end,
                }
                infos.append(info)
        return infos
