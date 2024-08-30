import json

from plone import api
from plone.dexterity.browser.view import DefaultView


class FullCalendarView(DefaultView):
    pass


class FullCalendarEventsView(DefaultView):
    @property
    def events(self):
        brains = api.content.find(
            context=self.context,
            portal_type="divingclub.Task",
            sort_on="start",
        )
        infos = []
        for b in brains:
            event = b.getObject()
            event_html = api.content.get_view("fullcalendar_view", event, self.request)()
            infos.append(
                {
                    "title": event.category_title + " / " + event.manager_fullname,
                    "category": event.category,
                    "category_title": event.category_title,
                    "manager": event.manager_fullname,
                    "start": event.start.isoformat() if event.start else None,
                    "end": event.end.isoformat() if event.end else None,
                    "event_html": event_html,
                }
            )
        return infos

    def __call__(self):
        data = json.dumps(self.events)
        self.request.response.setHeader("Content-type", "application/json; charset=utf-8")
        return data
