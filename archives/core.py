from belgium import BelgiumFindingAid
from fold3 import Fold3
from gettyas import GettyAS
from gettyri import GettyRI
from nara import NARACatalog
from ushmm import USHMM
from austria import AustriaFindingAid
from uk import UKFindingAid
from berlin import BerlinFindingAid
from netherlands import NetherlandsFindingAid
from bs4 import BeautifulSoup
import sys, logging

archivesList = [
     {
        'name': 'State Archives in Belgium',
        'logo': 'logo-state-archives-belgium.png',
        'info_url': 'http://www.archives.gov/research/holocaust/international-resources/belgium.html',
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
        'info_url': 'http://www.archives.gov/research/holocaust/international-resources/austria.html',
        'collections': [
            {
                'name': 'Holocaust Assets Finding Aid',
                'class': AustriaFindingAid.__name__,
                'lang': 'en'
            },
        ]
    },

    {
        'name': 'State Archives in UK',
        'logo': 'austria.png',
        'info_url': 'http://www.archives.gov/research/holocaust/international-resources/uk.html',
        'collections': [
            {
                'name': 'Holocaust Assets Finding Aid',
                'class': UKFindingAid.__name__,
                'lang': 'en'
            },
        ]
    },

    {
        'name': 'State Archives in Berlin',
        'logo': 'logo-bundesarchiv.png',
        'info_url': 'http://www.archives.gov/research/holocaust/international-resources/berlin.html',
        'collections': [
            {
                'name': 'Holocaust Assets Finding Aid',
                'class': BerlinFindingAid.__name__,
                'lang': 'en'
            },
        ]
    },

    {
        'name': 'State Archives in the Netherlands',
        'logo': 'logo-dhm.png',
        'info_url': 'http://www.archives.gov/research/holocaust/international-resources/netherlands.html',
        'collections': [
            {
                'name': 'Holocaust Assets Finding Aid',
                'class': NetherlandsFindingAid.__name__,
                'lang': 'en'
            },
        ]
    },
]
archivesList.sort(key=lambda inst: inst['name'])


def searchAll(rawinputs):
    async = True
    from multiprocessing.pool import ThreadPool
    pool = ThreadPool(processes=8)
    async_handles = []
    results = {}
    for inst in archivesList:
        for coll in inst['collections']:
            classname = coll['class']
            import sys
            module = sys.modules[__name__]
            collClass = getattr(module, classname)
            collObject = collClass()

            # NOTE: info.fields indicate advanced search support
            if hasattr(collObject, 'info'):
                if 'fields' in collObject.info:
                    inputs = rawinputs
                else:
                    inputs = rawinputs['general']
            else:
                inputs = rawinputs['general']

            if async:
                handle = pool.apply_async(collObject.keywordResultsCount, (inputs,))
                async_handles.append(handle)
            else:
                resultcoll = collObject.keywordResultsCount(inputs)
                result_dict = resultcoll.emit()
                results[result_dict['class']] = result_dict
    if async:
        for res in async_handles:
            try:
                resultcoll = res.get(timeout=15)
            except Exception, e:
                logging.exception(e)
                resultcoll = None
                pass
            if resultcoll != None:
                result_dict = resultcoll.emit()
                results[result_dict['class']] = result_dict
    return results
