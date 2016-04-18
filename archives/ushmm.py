# -*- coding: utf-8 -*-
from archives.collection import Collection
import requests
from bs4 import BeautifulSoup


class USHMM(Collection):

    info = {
        'name': 'Jeu de Paume',
        'class': 'USHMM',
        'lang': 'en',
        'fields': {
            'keywords': 'Solr__Query',
            'artist': 'Solr__Artist',
            'location': 'Solr__ObjectPostConfiscationHistory'
        }
    }

    def keywordResultsCount(self, **kwargs):
        params = self.mapParameters(kwargs, join_with='~ ')
        url = "http://www.errproject.org/jeudepaume/card_advanced_search.php"
        r = requests.get(url, params=params)
        html = r.text
        soup = BeautifulSoup(html, "lxml")
        results = soup.find_all("tr", class_="results")
        self.results_count = results.__len__()
        self.results_url = r.url
        return self
