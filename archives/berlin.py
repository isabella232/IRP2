__author__ = 'Anuj'
from collection import Collection
from bs4 import BeautifulSoup
import requests
import re
import json

class BerlinFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())
        url = "http://www.lostart.de/Webs/DE/Datenbank/SucheMeldungSimpel.html?resourceId=4424&input_=4046&pageLocale=de&simpel="+query+"&type=Simpel&type.HASH=a367122406f8d243ac08&suche_typ=MeldungSimpel&suche_typ.HASH=e2ace3636225271222d5&suchen=Suchen"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        #divs = soup.find_all('div')
        #print "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBb"
        #results = soup.find("div", {"id" : "id67734"})
        #results_1 = results.find("table", {"summary" : "suche0"})
        #results_2 = results_1.find("tbody")
        #results_3 = results_2.find_all("tr")
        #count =  results_3.__len__()

        results = soup.find("div", {"id" : "id67734"})
        results_1 = results.find("table", {"summary" : "suche0"})

        captionResults = results_1.find("caption")
        string1 = captionResults.string

        self.results_url = url
        self.results_count =  int(string1.split()[0])

        return self
