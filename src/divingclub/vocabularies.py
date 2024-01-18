from collective.taxonomy.interfaces import ITaxonomy
from zope.component import getUtility
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def vocabulary_from_items(items, add_none_value=False):
    terms = [SimpleTerm(value=key, token=str(key), title=value) for key, value in items.items()]
    if add_none_value:
        none_term = SimpleTerm(value=None, token=str(None), title="     ")
        terms.insert(0, none_term)
    return SimpleVocabulary(terms)


def get_title_from_vocabulary_value(vocabulary_name, vocabulary_value):
    factory = getUtility(IVocabularyFactory, vocabulary_name)
    vocabulary = factory(None)
    try:
        term = vocabulary.getTerm(vocabulary_value)
        return term.title
    except:
        return vocabulary_value


def get_title_from_taxonomy_value(taxonomy_name, taxonomie_value):
    taxonomy = getUtility(ITaxonomy, name=taxonomy_name)
    title = taxonomy.translate(taxonomie_value, target_language="fr")
    return title


DIVER_CATEGORIES = {
    "swimmer": "Nageur",
    "child0": "Plongeur enfant NH",
    "child1": "Dauphin de bronze",
    "child2": "Dauphin d'argent",
    "child3": "Dauphin d'or",
    "diver0": "Plongeur NH",
    "diver1": "Plongeur 1*",
    "diver2": "Plongeur 2*",
    "diver3": "Plongeur 3*",
    "diver3ppa": "Plongeur 3* PPA",
    "diver4": "Plongeur 4*",
    "instructor0": "Aide Moniteur",
    "instructor1": "Moniteur Club",
    "instructor2": "Moniteur Fédéral",
    "instructor3": "Moniteur National",
}

DIVER_CATEGORY_TO_GROUP = {
    "child0": "child",
    "child1": "child",
    "child2": "child",
    "child3": "child",
    "diver0": "zero",
    "diver1": "un",
    "diver2": "deux",
    "diver3": "trois",
    "diver3ppa": "trois",
    "diver4": "trois",
    "instructor0": "moniteur",
    "instructor1": "moniteur",
    "instructor2": "moniteur",
    "instructor3": "moniteur",
}
DIVER_CATEGORY_TO_ACRONYM = {
    "diver3ppa": "PPA",
    "diver4": "PPA",
    "instructor0": "AM",
    "instructor1": "MC",
    "instructor2": "MF",
    "instructor3": "MN",
}


@provider(IVocabularyFactory)
def get_diver_categories_vocabulary(context):
    return vocabulary_from_items(DIVER_CATEGORIES)
