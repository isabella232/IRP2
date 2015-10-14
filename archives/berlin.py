__author__ = 'Anuj'
from collection import Collection
from bs4 import BeautifulSoup
import requests
import json

class BerlinFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())
        url = "http://www.lostart.de/Content/051_ProvenienzRaubkunst/DE/AuktionInfo.html?Query="+query
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
