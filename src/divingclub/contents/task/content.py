from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone import schema
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from zope.interface import implementer

from divingclub.vocabularies import get_title_from_taxonomy_value


def get_default_manager():
    current_user_id = api.user.get_current().getId()
    if current_user_id == "admin":
        return None
    return current_user_id


class ITask(model.Schema):
    """Task interface"""

    # Fields
    category = schema.Choice(
        title="Catégorie",
        vocabulary="collective.taxonomy.task_categories",
    )
    manager = schema.Choice(
        title="Responsable",
        vocabulary="plone.app.vocabularies.Users",
        defaultFactory=get_default_manager,
    )

    # Widgets
    directives.widget("category", RadioFieldWidget)
    directives.widget("manager", AjaxSelectFieldWidget)


@implementer(ITask)
class Task(Item):
    """Task content type"""

    @property
    def category_title(self):
        return get_title_from_taxonomy_value("collective.taxonomy.task_categories", self.category)

    @property
    def title(self):
        computed_title = f"{self.category_title} /  {self.manager_fullname} / {self.start.date()}"
        return computed_title

    @title.setter
    def title(self, value):
        pass

    @property
    def location(self):
        return None  # La vue par défaut de Plone attend une 'location' pour les objet de type event

    @property
    def manager_fullname(self):
        user = api.user.get(userid=self.manager)
        user_fullname = user.getProperty("fullname") if user else self.manager
        return user_fullname
