from collection import Collection
import requests
from bs4 import BeautifulSoup

class USHMM(Collection):

    info = {
        'name': 'Jeu de Paume',
        'class': 'USHMM',
        'lang': 'en',
        'fields': {
            'general': 'Solr__Query',
            'artist': 'Solr__Artist',
            'location': 'Solr__ObjectPostConfiscationHistory'
        }
    }

    def keywordResultsCount(self, inputs):
        self.inputs = inputs['general']
        params = self.mapParameters(inputs)
        url = "http://www.errproject.org/jeudepaume/card_advanced_search.php"
        r = requests.get(url, params=params)
        html = r.text
        soup = BeautifulSoup(html, "lxml")

        results = soup.find_all("tr", class_="results")
        count = results.__len__()

        self.results_url = r.url
        self.results_count = count

        return self

