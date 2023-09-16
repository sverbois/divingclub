from collective.taxonomy.interfaces import ITaxonomy
from zope.component import getUtility
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def vocabulary_from_items(items, add_none_value=True):
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


DIVER_CERTIFICATES = {
    "swimmer": "Nageur",
    "child": "Plongeur enfant",
    "diver0": "Plongeur NH",
    "diver1": "Plongeur 1*",
    "diver2": "Plongeur 2*",
    "diver3": "Plongeur 3*",
    "diver3ppa": "Plongeur 3* PPA",
    "diver4": "Plongeur 4*",
    "instructor0": "Aide moniteur",
    "instructor1": "Moniteur club",
    "instructor2": "Moniteur fédéral",
    "instructor3": "Moniteur national",
}


@provider(IVocabularyFactory)
def get_divercertificates_vocabulary(context):
    return vocabulary_from_items(DIVER_CERTIFICATES)
