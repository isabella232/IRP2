__author__ = 'anuj'
from collection import Collection
from bs4 import BeautifulSoup 
import requests
import json

class UKFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())
        url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+query+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        results = soup.find_all("li", class_="tna-result")
        count = results.__len__()

        self.results_url = url
        self.results_count = count

        return self