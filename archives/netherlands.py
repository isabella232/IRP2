__author__ = 'Anuj'
from collection import Collection
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import json

class NetherlandsFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        print 'netherlands : '+ inputs

        #query = "+".join(inputs.split())

        query = inputs.split(' ')
        x=len(query)
        print x

        if (x>1):
         try:
            blob = TextBlob(query[1])
            if (query[0]=='German'):
                query_german = blob.translate(to="de")
                self.result_search_term = str(query_german)
                url = "http://www.archieven.nl/nl/zoeken?mizig=0&miview=lst&milang=nl&micols=1&mires=0&mizk_alle="+str(query_german)
            elif (query[0]=='French') :
                query_french = blob.translate(to="fr")
                self.result_search_term = str(query_french)
                url = "http://www.archieven.nl/nl/zoeken?mizig=0&miview=lst&milang=nl&micols=1&mires=0&mizk_alle="+str(query_french)
         except:
             url = "http://www.archieven.nl/nl/zoeken?mizig=0&miview=lst&milang=nl&micols=1&mires=0&mizk_alle="+query[0]
             pass
        else:
          url = "http://www.archieven.nl/nl/zoeken?mizig=0&miview=lst&milang=nl&micols=1&mires=0&mizk_alle="+query[0]
          self.result_search_term = query[0]

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


