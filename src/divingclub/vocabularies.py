from collective.taxonomy.interfaces import ITaxonomy
from zope.component import getUtility
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def vocabulary_from_items(items, add_none_value=True):
    terms = [SimpleTerm(value=key, token=str(key), title=value) for key, value in items.iteritems()]
    if add_none_value:
        none_term = SimpleTerm(value=None, token=str(None), title="     ")
        terms.insert(0, none_term)
    return SimpleVocabulary(terms)


def get_title_from_taxonomy_value(taxonomy_name, taxonomie_value):
    taxonomy = getUtility(ITaxonomy, name=taxonomy_name)
    title = taxonomy.translate(taxonomie_value, target_language="fr")
    return title


EXAMPLE = {
    "bar": "Bar",
    "inflation": "Gonflage",
    "pool": "Surveillance piscine",
}


def get_EXAMPLE_vocabulary(context):
    return vocabulary_from_items(EXAMPLE)
