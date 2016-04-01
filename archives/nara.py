# -*- coding: utf-8 -*-
from collection import Collection
import requests
from textblob import TextBlob

class NARACatalog(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        #query = "+".join(inputs.split())

        query = inputs.split(' ',1)
        x=len(query)
        print x

        if (x>1):
          try:
            blob = TextBlob(query[1])
            if (query[0]=='German'):
                query_german = blob.translate(to="de")
                query_german = unicode( query_german, "utf-8" )
                url = "https://catalog.archives.gov/api/v1/?q="+str(query_german)
                self.results_url = "https://catalog.archives.gov/search?q="+str(query_german)
                self.result_search_term = str(query_german)
                self.result_search_term = self.result_search_term.encode('utf-8')

            elif (query[0]=='French') :
                query_french = blob.translate(to="fr")
                query_french = unicode( query_french, "utf-8" )
                url = "https://catalog.archives.gov/api/v1/?q="+str(query_french)
                self.results_url = "https://catalog.archives.gov/search?q="+str(query_french)
                self.result_search_term = str(query_french)
                self.result_search_term = self.result_search_term.encode('utf-8')

            else :
                query1 = " "+ inputs
                query1 = query1.split(' ',1)
                url = "https://catalog.archives.gov/api/v1/?q="+str(query1[1])
                self.results_url = "https://catalog.archives.gov/search?q="+query1[1]
                self.result_search_term = query1[1]


          except:
              url = "https://catalog.archives.gov/api/v1/?q="+str(query[1])
              self.results_url = "https://catalog.archives.gov/search?q="+query[1]
              self.result_search_term = query[1]
              pass
        else:
          url = "https://catalog.archives.gov/api/v1/?q="+str(query[0])
          self.results_url = "https://catalog.archives.gov/search?q="+query[0]
          self.result_search_term = query[0]

        res = requests.get(url)
        parsed = res.json()
        num = parsed["opaResponse"]["results"]["total"]


        #self.results_url = "https://catalog.archives.gov/search?q="+query
        if num!= None:
            self.results_count = num
        else:
            self.results_count = 0
        return self
