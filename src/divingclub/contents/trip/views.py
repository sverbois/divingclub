import json
import subprocess
import tempfile

from plone import api
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser import BrowserView

from divingclub.vocabularies import DIVER_CATEGORY_TO_ACRONYM
from divingclub.vocabularies import DIVER_CATEGORY_TO_COLOR
from divingclub.vocabularies import DIVER_CATEGORY_TO_GROUP

STATE_INFOS = {
    "pending": {"title": "A confirmer", "color": "warning"},
    "accepted": {"title": "Acceptée", "color": "success"},
    "declined": {"title": "Refusée", "color": "danger"},
}


def get_registrations(trip, only_accepted=False):
    filters = {
        "context": trip,
        "depth": 1,
        "portal_type": "divingclub.Registration",
        "sort_on": "getObjPositionInParent",
    }
    if only_accepted:
        filters["review_state"] = "accepted"
    brains = api.content.find(**filters)
    return [b.getObject() for b in brains]


class TripView(DefaultView):
    """Trip view"""

    @property
    def registrations(self):
        items = get_registrations(self.context)
        infos = []
        for registration in items:
            review_state = api.content.get_state(registration)
            infos.append(
                {
                    "fullname": registration.participant_fullname,
                    "category": registration.participant_category,
                    "email": registration.participant_email,
                    "url": self.context.absolute_url() + "/" + registration.getId(),
                    "whish": registration.whish,
                    "state": review_state,
                    "state_title": STATE_INFOS[review_state]["title"],
                    "color": STATE_INFOS[review_state]["color"],
                    "editable": api.user.has_permission("Modify portal content", obj=registration),
                }
            )
        return infos


class TripSheetView(BrowserView):
    @property
    def current_user(self):
        return api.user.get_current()

    @property
    def registrations_by_team(self):
        registrations_by_team = {i: [] for i in range(1, 16)}
        teams = self.context.teams
        for number, team in enumerate(teams):
            for uid in team:
                registration = api.content.get(UID=uid)
                if registration:
                    user = registration.user
                    category = user.getProperty("diver_category")
                    registrations_by_team[number + 1].append(
                        {
                            "fullname": registration.participant_fullname[:20],
                            "category": DIVER_CATEGORY_TO_ACRONYM.get(category),
                        }
                    )
        return registrations_by_team

    @property
    def registrations_by_group(self):
        items = get_registrations(self.context, only_accepted=True)
        infos = {
            "moniteur": [],
            "trois": [],
            "deux": [],
            "un": [],
            "zero": [],
            "child": [],
        }
        for r in items:
            user = r.user
            firstname = user.getProperty("firstname")
            lastname = user.getProperty("lastname")
            category = user.getProperty("diver_category")
            group = DIVER_CATEGORY_TO_GROUP.get(category)
            if category.startswith("instructor") or category.startswith("child"):
                fullname = f"{lastname} {firstname[:1]}."
            else:
                fullname = f"{lastname} {firstname}"
            if group == "moniteur":
                user_info = DIVER_CATEGORY_TO_ACRONYM.get(category)
            elif group == "trois":
                user_info = "4*" if category in ("diver3ppa", "diver4") else "3*"
            else:
                user_info = ""
            if group in infos:
                infos[group].append(
                    {
                        "fullname": fullname,
                        "info": user_info,
                        "whish": r.whish.strip() if r.whish else "",
                    }
                )
        # ADD Empty users to fill the table
        for group in infos.values():
            empty_group_count = 9 - len(group)
            for num in range(empty_group_count):
                group.append({"fullname": "", "info": "", "whish": ""})
        return infos

    @property
    def registrations_with_whish(self):
        return [r for group in self.registrations_by_group.values() for r in group if r["whish"]]


class TripSheetPdfView(BrowserView):

    def __call__(self):
        html_view = api.content.get_view(name="registration-sheet-html", context=self.context, request=self.request)
        html = html_view().encode("utf-8")

        html_file = tempfile.NamedTemporaryFile(suffix=".html")
        html_file.write(html)
        html_file.flush()
        pdf_file = tempfile.NamedTemporaryFile(suffix=".pdf")
        subprocess.call(
            [
                "wkhtmltopdf",
                "--quiet",
                "--print-media-type",
                "--page-size",
                "A4",
                "--margin-top",
                "10mm",
                "--margin-bottom",
                "5mm",
                "--margin-left",
                "5mm",
                "--margin-right",
                "5mm",
                html_file.name,
                pdf_file.name,
            ]
        )

        filename = f"{self.context.title}.pdf"
        self.request.response.setHeader("Content-Type", "application/pdf")
        self.request.response.setHeader("Content-Disposition", "inline;filename={}".format(filename))
        return pdf_file.read()


class MakeTeamsView(BrowserView):
    def _get_registration_infos(self, registration):
        uid = registration.UID()
        user = registration.user
        category = user.getProperty("diver_category")
        return {
            "uid": uid,
            "fullname": registration.participant_fullname[:20],
            "category": DIVER_CATEGORY_TO_ACRONYM.get(category),
            "color": DIVER_CATEGORY_TO_COLOR.get(category, "dark"),
        }

    @property
    def registrations(self):
        registrations = get_registrations(self.context, only_accepted=True)
        uid_to_registrations = {r.UID(): r for r in registrations}
        teams = self.context.teams
        infos = []
        for number, team in enumerate(teams):
            team_number = number + 1
            for uid in team:
                if uid in uid_to_registrations:
                    registration = uid_to_registrations.pop(uid)
                    registration_infos = self._get_registration_infos(registration)
                    registration_infos["team"] = team_number
                    infos.append(registration_infos)
        for registration in uid_to_registrations.values():
            registration_infos = self._get_registration_infos(registration)
            registration_infos["team"] = 0
            infos.append(registration_infos)
        return infos


class StoreTeamsView(BrowserView):
    def __call__(self):
        if self.request.method == "POST":
            json_teams = self.request.form.get("teams")
            if json_teams:
                self.context.teams = json.loads(json_teams)
                self.context.reindexObject()
                api.portal.show_message(message="L'organisattion des palanquées a été sauvée.", type="info")
        return self.request.response.redirect(self.context.absolute_url())
