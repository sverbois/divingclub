import json

from plone import api
from plone.dexterity.browser.view import DefaultView


class FullCalendarView(DefaultView):
    pass


class FullCalendarEventsView(DefaultView):
    @property
    def events(self):
        portal_url = api.portal.get().absolute_url()
        brains = api.content.find(
            context=self.context,
            portal_type="divingclub.Task",
            sort_on="start",
        )
        infos = []
        for b in brains:
            event = b.getObject()
            event_url = event.absolute_url()
            is_editor = api.user.has_permission("Modify portal content", obj=event)
            infos_html = f"""<strong>{event.category_title}</strong><br />{event.manager_fullname}"""
            history_html = (
                f"""<a href="{event_url}/@@historyview" class="float-end  ps-3"><img src="{portal_url}/++plone++bootstrap-icons/clock.svg" /></a>"""
                if is_editor
                else ""
            )
            edit_html = (
                f"""<a href="{event_url}/@@edit" class="float-end  ps-3"><img src="{portal_url}/++plone++bootstrap-icons/pencil.svg" /></a>"""
                if is_editor
                else ""
            )
            delete_html = (
                f"""<a href="{event_url}/@@delete_confirmation" class="float-end ps-3"><img src="{portal_url}/++plone++bootstrap-icons/trash.svg" /></a>"""
                if is_editor
                else ""
            )
            event_html = f"<div>{delete_html}{edit_html}{history_html}{infos_html}</div>"
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
