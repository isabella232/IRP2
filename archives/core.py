from belgium import BelgiumFindingAid
from fold3 import Fold3
from gettyas import GettyAS
from gettyri import GettyRI
from nara import NARACatalog
from ushmm import USHMM
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
                'name': 'USHMM Catalog',
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
            async_results.append(pool.apply_async(collObject.keywordResultsCount, (inputs,)))
    results = {}
    for res in async_results:
        result_dict = res.get().emit()
        results[result_dict['class']] = result_dict
    return results
