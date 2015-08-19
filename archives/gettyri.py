__author__ = 'gregjan'
from collection import Collection
from bs4 import BeautifulSoup
import requests

class GettyRI(Collection):
    results_count = None
    results_url = None
    inputs = None

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())
        url = "http://www.getty.edu/Search/SearchServlet?qt="+query
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        table = soup.find_all("table")[2]
        num = table.find("td").contents[0].strip().split()
        count = num[1]

        self.results_url = url
        if (count.isdigit()):
             self.results_count = count
        else:
             self.results_count = 0
        return self
