__author__ = 'Anuj'
from collection import Collection
from bs4 import BeautifulSoup
import requests
import json

class NetherlandsFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())

        url = "http://www.archieven.nl/nl/zoeken?mizig=0&miview=lst&milang=nl&micols=1&mires=0&mizk_alle="+query
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        spanList = soup.select('span.mi_hits_hits_count')
        num = None
        s = spanList[0].string

        if len(s)>0:
            num = int(s)

        self.results_url = url
        self.results_count = num

        return self


