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

        num = soup.find("div",class_="num")
        if num!= None:
            counts = num.contents[0]
            count = counts.split()[5]
        else:
            count = 0

        self.results_url = url
        self.results_count = count

        return self
