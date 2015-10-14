from collection import Collection
import requests
from bs4 import BeautifulSoup 

class USHMM(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())

        url = "http://www.errproject.org/jeudepaume/card_search.php?Query=" + query
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        results = soup.find_all("tr", class_="results")
        count = results.__len__()

        self.results_url = url
        self.results_count = count

        return self

