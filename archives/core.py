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
import sys 

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
            {
                'name': 'Jeu de Paume',
                'class': USHMM.__name__,
                'lang': 'en'
            }
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
            {
                'name': 'Fold3 Holocaust Era Assets',
                'class': Fold3.__name__,
                'lang': 'en'
            }
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


def searchAllParallel(inputs):
    from multiprocessing.pool import ThreadPool
    pool = ThreadPool(processes=8)
    async_results = []

    for inst in archivesList:
        for coll in inst['collections']:
            classname = coll['class']
            import sys
            module = sys.modules[__name__]
            collClass = getattr(module, classname)
            collObject = collClass()
            handle = pool.apply_async(collObject.keywordResultsCount, (inputs,))
            async_results.append(handle)
    results = {}
    for res in async_results:
        try:
            resultcoll = res.get(timeout=10)
        except TimeoutError:
            pass
        if resultcoll != None:
            result_dict = resultcoll.emit()
            results[result_dict['class']] = result_dict
    return results

