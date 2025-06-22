import datetime

from plone import api
from plone import schema
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from zope.interface import implementer
from divingclub.vocabularies import CASHBOXSTATUS_CATEGORIES

def get_default_cashier():
    current_user_id = api.user.get_current().getId()
    if current_user_id == "admin":
        return None
    return current_user_id


def get_default_datetime():
    return datetime.datetime.now()


class ICashBoxStatus(model.Schema):
    """Cash Box Status interface"""

    # Fields
    cashier = schema.Choice(
        title="Caissier",
        vocabulary="plone.app.vocabularies.Users",
        defaultFactory=get_default_cashier,
    )
    datetime = schema.name = schema.Datetime(
        title="Date et heure",
        description="Indiquer la date et l'heure de l'ouverture/fermeture de la caisse.",
        defaultFactory=get_default_datetime,
    )
    category = schema.Choice(
        title="Ouverture/Fermeture",
        vocabulary="divingclub.CashBoxStatusCategories",
    )
    banknote5 = schema.Int(
        title="Billets de 5€",
        description="Indiquer le nombre de billets de 5€ dans la caisse.",
        default=0,
    )
    banknote10 = schema.Int(
        title="Billets de 10€",
        description="Indiquer le nombre de billets de 10€ dans la caisse.",
        default=0,
    )
    banknote20 = schema.Int(
        title="Billets de 20€",
        description="Indiquer le nombre de billets de 20€ dans la caisse.",
        default=0,
    )
    banknote50 = schema.Int(
        title="Billets de 50€",
        description="Indiquer le nombre de billets de 50€ dans la caisse.",
        default=0,
    )
    banknote100 = schema.Int(
        title="Billets de 100€",
        description="Indiquer le nombre de billets de 100€ dans la caisse.",
        default=0,
    )
    coin5 = schema.Int(
        title="Pièces de 5c",
        description="Indiquer le nombre de pièces de 5c dans la caisse.",
        default=0,
    )
    coin10 = schema.Int(
        title="Pièces de 10c",
        description="Indiquer le nombre de pièces de 10c dans la caisse.",
        default=0,
    )
    coin20 = schema.Int(
        title="Pièces de 20c",
        description="Indiquer le nombre de pièces de 20c dans la caisse.",
        default=0,
    )
    coin50 = schema.Int(
        title="Pièces de 50c",
        description="Indiquer le nombre de pièces de 50c dans la caisse.",
        default=0,
    )

    # Widgets
    directives.widget("category", RadioFieldWidget)
    directives.widget("cashier", AjaxSelectFieldWidget)


@implementer(ICashBoxStatus)
class CashBoxStatus(Item):
    """Cash Box Status content type"""

    @property
    def title(self):
        category_title = CASHBOXSTATUS_CATEGORIES.get(self.category, self.category)
        computed_title = f"{category_title} caisse le {self.datetime}"
        return computed_title

    @title.setter
    def title(self, value):
        pass

    @property
    def cashier_fullname(self):
        user = api.user.get(userid=self.cashier)
        user_fullname = user.getProperty("firstname") + " " + user.getProperty("lastname") if user else self.cashier
        return user_fullname

    @property
    def total(self):
        total = (
            self.banknote5 * 5
            + self.banknote10 * 10
            + self.banknote20 * 20
            + self.banknote50 * 50
            + self.banknote100 * 100
            + self.coin5 * 0.05
            + self.coin10 * 0.1
            + self.coin20 * 0.2
            + self.coin50 * 0.5
        )
        return total
