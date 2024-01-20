from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone import schema
from plone.app.z3cform.widgets.select import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from zope.interface import implementer

from divingclub.vocabularies import get_title_from_taxonomy_value


class ITrip(model.Schema):
    """Trip interface"""

    # Fields
    spot = schema.Choice(
        title="Lieu de plongée",
        vocabulary="collective.taxonomy.trip_spots",
    )
    manager = schema.Choice(
        title="Responsable",
        vocabulary="plone.app.vocabularies.Users",
    )
    description = schema.Text(
        title="Commentaires",
        required=False,
    )

    # Widgets
    directives.widget("manager", AjaxSelectFieldWidget)


@implementer(ITrip)
class Trip(Container):
    """Trip content type"""

    def canSetDefaultPage(self):
        return False

    @property
    def location(self):
        return get_title_from_taxonomy_value("collective.taxonomy.trip_spots", self.spot)

    @property
    def title(self):
        computed_title = f"Sortie {self.location} le {self.start.date()}"
        return computed_title

    @title.setter
    def title(self, value):
        pass

    @property
    def manager_fullname(self):
        user = api.user.get(userid=self.manager)
        user_fullname = user.getProperty("fullname") if user else self.manager
        return user_fullname

    @property
    def participants(self):
        return [r.participant for r in self.values() if r.portal_type == "divingclub.Registration"]
