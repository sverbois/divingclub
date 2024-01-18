from plone import api

from divingclub.vocabularies import DIVER_CATEGORY_TO_GROUP


def on_add_registration(registration, event):
    with api.env.adopt_user(username="admin"):
        user = registration.user
        category = user.getProperty("diver_category")
        group = DIVER_CATEGORY_TO_GROUP.get(category)
        if group in ("moniteur", "trois", "deux"):
            api.content.transition(obj=registration, transition="make_accepted")
