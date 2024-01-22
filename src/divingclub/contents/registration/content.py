from Acquisition import aq_parent
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone import schema
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form import validator
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope.interface import Invalid
from zope.interface import implementer

from divingclub.vocabularies import get_title_from_vocabulary_value


def default_participant():
    current_user_id = api.user.get_current().getId()
    if current_user_id == "admin":
        return None
    return current_user_id


class IRegistration(model.Schema):
    """Registration interface"""

    participant = schema.Choice(
        title="Participant",
        vocabulary="plone.app.vocabularies.Users",
        defaultFactory=default_participant,
    )
    whish = schema.Text(
        title="Desiterata",
        description="Indiquer si vous désirez effectuer un exercie ou si vous avez d'autres souhaits.",
        required=False,
    )

    # Widgets
    directives.widget("participant", AjaxSelectFieldWidget)


class ParticipantValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        if IAddForm.providedBy(self.view):
            trip = self.context
            if value in trip.participants:
                raise Invalid("Ce membre est déjà inscrit à la sortie.")
        elif IEditForm.providedBy(self.view):
            trip = aq_parent(self.context)
            if (value != self.context.participant) and (value in trip.participants):
                raise Invalid("Ce membre est déjà inscrit à la sortie.")


validator.WidgetValidatorDiscriminators(ParticipantValidator, field=IRegistration["participant"])


@implementer(IRegistration)
class Registration(Item):
    """Registration content type"""

    @property
    def title(self):
        computed_title = f"{self.participant_fullname} - {self.participant_category}"
        return computed_title

    @title.setter
    def title(self, value):
        pass

    @property
    def user(self):
        return api.user.get(userid=self.participant)

    @property
    def participant_fullname(self):
        user = self.user
        user_fullname = user.getProperty("fullname") if user else self.participant
        return user_fullname

    @property
    def participant_email(self):
        user = self.user
        user_email = user.getProperty("email") if user else ""
        return user_email

    @property
    def participant_category(self):
        user = api.user.get(userid=self.participant)
        user_category = user.getProperty("diver_category") if user else ""
        user_category_title = get_title_from_vocabulary_value("divingclub.DiverCategories", user_category)
        return user_category_title
