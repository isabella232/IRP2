__author__ = 'Anuj'
from collection import Collection
from bs4 import BeautifulSoup
import requests
import json

class NetherlandsFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())

        url = "http://www.archieven.nl/nl/result-modonly?miview=inv2&mivast=298&mizig=210&miadt=298&micode=093a&milang=nl?Query=" + query
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        results = soup.find_all("tr", class_="results")
        count = results.__len__()

        self.results_url = url
        self.results_count = count

        return self


