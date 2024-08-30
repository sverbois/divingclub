from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from datetime import timezone

from plone import api
from Products.Five.browser import BrowserView


class WeekItemView(BrowserView):
    """Task view"""

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
        todo_title = "A faire" if self.context.start > datetime.now(timezone.utc) else "A confirmer"
        state_infos = {
            "todo": {"title": todo_title, "color": "warning"},
            "performed": {"title": "Réalisée", "color": "success"},
            "notperformed": {"title": "Non réalisée", "color": "danger"},
        }
        state = api.content.get_state(self.context)
        return state_infos.get(state, {"title": state, "color": "secondary"})


class WeekListingView(BrowserView):
    """Listing view"""

    def __init__(self, context, request):
        super().__init__(context, request)
        # Compute start and end datetime
        request_week = request.form.get("week", None)
        request_year = request.form.get("year", None) if request_week else None
        year = int(request_year) if request_year else date.today().year
        week = int(request_week) if request_week else date.today().isocalendar()[1]
        start_date = date.fromisocalendar(year, week, 1)
        end_date = date.fromisocalendar(year, week, 7)
        self.year = year
        self.week = week
        self.start_datetime = datetime.combine(start_date, time.min)
        self.end_datetime = datetime.combine(end_date, time.max)
        self._compute_links()

    def _compute_links(self):
        start_date = self.start_datetime.date()
        previous_week_start_date = start_date - timedelta(days=7)
        previous_week = previous_week_start_date.isocalendar()[1]
        previous_year = previous_week_start_date.isocalendar()[0]
        next_week_start_date = start_date + timedelta(days=7)
        next_week = next_week_start_date.isocalendar()[1]
        next_year = next_week_start_date.isocalendar()[0]
        self.previous_listing_url = (
            f"{self.context.absolute_url()}/@@week_listing?week={previous_week}&year={previous_year}"
        )
        self.next_listing_url = f"{self.context.absolute_url()}/@@week_listing?week={next_week}&year={next_year}"

    @property
    def tasks_by_day(self):
        start_date_query = {
            "query": (self.start_datetime, self.end_datetime),
            "range": "min:max",
        }
        brains = api.content.find(
            context=self.context,
            portal_type="divingclub.Task",
            start=start_date_query,
            sort_on="start",
        )
        tasks = [b.getObject() for b in brains]
        by_day = {}
        for task in tasks:
            day = task.start.date()
            by_day.setdefault(day, []).append(task)
        return by_day


class WeekViewView(BrowserView):
    """Week view"""

    pass
