from archives.dummy import Dummy
from archives.belgium import BelgiumFindingAid
from archives.fold3 import Fold3
from archives.gettyas import GettyAS
from archives.gettyri import GettyRI
from archives.nara import NARACatalog
from archives.ushmm import USHMM
from archives.austria import AustriaFindingAid
from archives.uk import UKFindingAid
from archives.netherlands import NetherlandsFindingAid
from archives.lost_art import LostArt
import sys
import json
import logging
from textblob import TextBlob
from textblob.translate import NotTranslated

archivesList = [
    {
        'name': 'State Archives in Belgium',
        'logo': 'logo-state-archives-belgium.png',
        'info_url': "http://www.archives.gov/research/holocaust/international-resources/"
                    "belgium.html",
        'collections': [
            {
                'name': 'Holocaust Assets Finding Aid',
                'class': BelgiumFindingAid.__name__,
                'lang': 'en'
            },
        ]
    },
    {
        'name': 'Getty Research Institute',
        'logo': 'getty.jpg',
        'info_url': 'http://www.getty.edu/museum/research/provenance/index.html',
        'collections': [
            {
                'name': 'German Art Sales Catalogs',
                'class': GettyAS.__name__,
                'lang': 'de'
            },
            {
                'name': 'Getty Catalog',
                'class': GettyRI.__name__,
                'lang': 'en'
            }
        ]
    },
    {
        'name': 'United States Holocaust Memorial Museum',
        'logo': 'logo-ushmm.png',
        'info_url': 'http://www.ushmm.org/research/research-in-collections/overview',
        'collections': [
            USHMM.info
        ]
    },
    {
        'name': 'United States National Archives and Records Administration',
        'logo': 'logo-nara.png',
        'info_url': 'http://www.archives.gov/research/',
        'collections': [
            {
                'name': 'NARA Catalog',
                'class': NARACatalog.__name__,
                'lang': 'en'
            },
            Fold3.info
        ]
    },
    {
        'name': 'State Archives in Austria',
        'logo': 'austria.png',
        'info_url': 'http://www.archives.gov/research/holocaust/international-resources/'
                    'austria.html',
        'collections': [
            {
                'name': 'Art Database of the National Fund',
                'class': AustriaFindingAid.__name__,
                'lang': 'en'
            },
        ]
    },
    {
        'name': 'National Archives of the UK',
        'logo': 'austria.png',
        'info_url': 'http://www.archives.gov/research/holocaust/international-resources/uk.html',
        'collections': [
            {
                'name': 'The National Archives',
                'class': UKFindingAid.__name__,
                'lang': 'en'
            },
        ]
    },

    {
        'name': 'Federal Archives of Germany',
        'logo': 'logo-bundesarchiv.png',
        'info_url': 'http://www.archives.gov/research/holocaust/international-resources/'
                    'bundesarchiv.html',
        'collections': [
            {
                'name': 'Lost Art Database (Magdeburg)',
                'class': LostArt.__name__,
                'lang': 'en'
            },
        ]
    },
    {
        'name': 'State Archives in the Netherlands',
        'logo': 'logo-dhm.png',
        'info_url': 'http://www.archives.gov/research/holocaust/international-resources/'
                    'netherlands.html',
        'collections': [
            {
                'name': 'Archives and Collections',
                'class': NetherlandsFindingAid.__name__,
                'lang': 'en'
            },
        ]
    },
]


archivesList.sort(key=lambda inst: inst['name'])


def get_translations(keywords, languages):
    result = []
    if len(languages) > 0:
        blob = TextBlob(keywords)
        for lang in languages:
            try:
                result.append(str(blob.translate(to=lang)))
            except NotTranslated:
                pass
    return result


# asyncSearch - Set to False for serial searches and better error reporting
# dummySearch - Set to True for offline development work w/o searches
def searchAll(**kwargs):
    """Search all known collections for the given input dictionary."""
    logging.debug('searchAll called:\n{0}'.format(json.dumps(kwargs)))
    dummySearch = False
    from multiprocessing.pool import ThreadPool
    pool = ThreadPool(processes=10)
    async_handles = []
    terms = kwargs.get('translated_terms', '')
    results = {'collections': {}, 'translated_terms': terms}
    for inst in archivesList:
        for coll in inst['collections']:
            classname = coll['class']
            module = sys.modules[__name__]
            collClass = getattr(module, classname)
            collObject = collClass()

            if dummySearch:  # use dummy collection that does no search..
                collObject = Dummy()
                collObject.setClassName(classname)

            handle = pool.apply_async(collObject.keywordResultsCount, (), kwargs)
            async_handles.append(handle)

    # NOTE: Maintain indent level, do not put this inside above FOR loop
    for res in async_handles:
        try:
            resultcoll = res.get(timeout=15)
        except Exception as e:
            logging.exception(e)
            resultcoll = None
            pass
        if resultcoll is not None:
            result_dict = resultcoll.emit()
            results['collections'][result_dict['class']] = result_dict
    return results
