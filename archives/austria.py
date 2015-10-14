__author__ = 'anuj'
from collection import Collection
from bs4 import BeautifulSoup 
import requests
import json

class AustriaFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())
        url = "http://www.kunstrestitution.at/catalogue.html?Query="+query
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        results = soup.find_all("div", class_="item")
        count = results.__len__()

        self.results_url = url
        self.results_count = count

        return self
