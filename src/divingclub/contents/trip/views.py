from plone import api
from plone.dexterity.browser.view import DefaultView

STATE_INFOS = {
    "pending": {"title": "A confirmer", "color": "warning"},
    "accepted": {"title": "Acceptée", "color": "success"},
    "declined": {"title": "Refusée", "color": "danger"},
}


class TripView(DefaultView):
    """Trip view"""

    @property
    def registrations(self):
        wtool = api.portal.get_tool("portal_workflow")
        brains = api.content.find(
            context=self.context,
            depth=1,
            portal_type="divingclub.Registration",
            sort_on="getObjPositionInParent",
        )
        items = [b.getObject() for b in brains]
        infos = []
        for registration in items:
            review_state = wtool.getInfoFor(registration, "review_state", None)
            infos.append(
                {
                    "fullname": registration.participant_fullname,
                    "category": registration.participant_category,
                    "url": self.context.absolute_url() + "/" + registration.getId(),
                    "whish": registration.whish,
                    "state": STATE_INFOS[review_state]["title"],
                    "color": STATE_INFOS[review_state]["color"],
                    "editable": api.user.has_permission("Modify portal content", obj=registration),
                }
            )
        return infos
