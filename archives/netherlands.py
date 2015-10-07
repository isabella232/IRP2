__author__ = 'Anuj'
from collection import Collection
from bs4 import BeautifulSoup
import requests
import json

class NetherlandsFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())
        url = "https://catalog.archives.gov/api/v1/?q="+query
        res = requests.get(url)
        parsed = res.json()
        num = parsed["opaResponse"]["results"]["total"]

        self.results_url = "http://search.archives.gov/query.html?qt="+query
        if num!= None:
            self.results_count = num
        else:
            self.results_count = 0
        return self

