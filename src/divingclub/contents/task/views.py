import datetime
import locale

from plone import api
from Products.Five.browser import BrowserView

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


class TaskView(BrowserView):
    """Task view"""

    def __call__(self):
        parent = self.context.__parent__
        parent_url = parent.absolute_url()
        year = self.context.start.year
        week = self.context.start.isocalendar()[1]
        url = f"{parent_url}?week={week}&year={year}"
        self.request.response.redirect(url)


class TaskFullCalendarView(BrowserView):
    """Task FullCalendar view"""

    @property
    def portal_url(self):
        return api.portal.get().absolute_url()

    @property
    def is_editor(self):
        return api.user.has_permission("Modify portal content", obj=self.context)

    @property
    def is_reviewer(self):
        user = api.user.get_current()
        return user and (user.has_role("Reviewer", self.context) or user.has_role("Manager", self.context))

    @property
    def state(self):
        todo_title = "A faire" if self.context.start > datetime.datetime.now(datetime.timezone.utc) else "A confirmer"
        state_infos = {
            "todo": {"title": todo_title, "color": "warning"},
            "performed": {"title": "Réalisée", "color": "success"},
            "notperformed": {"title": "Non réalisée", "color": "danger"},
        }
        state = api.content.get_state(self.context)
        return state_infos.get(state, {"title": state, "color": "secondary"})
