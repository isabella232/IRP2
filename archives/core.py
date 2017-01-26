from archives.dummy import Dummy
from archives.belgium import BelgiumFindingAid
from archives.fold3 import ArdeliaHall
from archives.gettyas import GettyAS
from archives.nara import NARACatalog
from archives.ushmm import JeuDePaume
from archives.austria import AustriaArtDB
from archives.uk import UKCollection
from archives.netherlands import NetherlandsStateArchives
from archives.lost_art import LostArt
from archives.DHMMunich import DHMMunich
from archives.MemorialSHOAH import MemorialSHOAH
import sys
import json
import logging
from google.cloud import translate


gclient = translate.Client()


def get_translations(keywords, languages):
    result = []
    if len(languages) > 0:
        for lang in languages:
            try:
                reply = gclient.translate(keywords, target_language=lang)
                result.append(str(reply['translatedText']))
            except Exception as e:  # NotTranslated
                logging.warn(e)
    return result


def search(**kwargs):
    """Search a collection for relevant results"""
    logging.debug('search called:\n{0}'.format(json.dumps(kwargs)))
    terms = kwargs.get('translated_terms', '')
    classname = kwargs['collectionid']
    module = sys.modules[__name__]
    collClass = getattr(module, classname)
    collObject = collClass()
    from multiprocessing.pool import ThreadPool
    pool = ThreadPool(processes=1)
    handle = pool.apply_async(collObject.keywordResultsCount, (), kwargs)
    resultcoll = None
    try:
        resultcoll = handle.get(timeout=20)
    except Exception as e:
        logging.exception(e)
        result = {'error': "Site not responding"}
        pass
    if resultcoll is not None:
        result = resultcoll.emit()

    result['translated_terms'] = str(terms)
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
