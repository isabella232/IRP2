__author__ = 'anuj'
from collection import Collection
from bs4 import BeautifulSoup 
import requests
import json

class AustriaFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        session = requests.session()
        data = {}
        data['search'] = inputs

        url = "http://www.kunstrestitution.at/catalogue_detailsearch.html"
        r = session.post(url,data = data)
        soup = BeautifulSoup(r.text, "lxml")

        spanList = soup.select('span.total')
        num = None
        s = spanList[0].string

        newString = s[s.find("(")+1:s.find(")")]

        if len(newString)>0:
            num = int(newString)

        self.results_url = url

        if num!= None:
            self.results_count = num
        else:
            self.results_count = 0

        #results = soup.find_all("div",class_="item")
        #count = results.__len__()

        #self.results_url = url
        #self.results_count = count

        return self
