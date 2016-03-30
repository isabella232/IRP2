from collection import Collection
from bs4 import BeautifulSoup 
import requests
import json
from textblob import TextBlob

class NARACatalog(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        #query = "+".join(inputs.split())

        query = inputs.split(' ')
        x=len(query)
        print x

        if (x>1):
          try:
            blob = TextBlob(query[1])
            if (query[0]=='German'):
                query_german = blob.translate(to="de")
                url = "https://catalog.archives.gov/api/v1/?q="+str(query_german)
                self.results_url = "https://catalog.archives.gov/search?q="+str(query_german)
                self.result_search_term = str(query_german)

            elif (query[0]=='French') :
                query_french = blob.translate(to="fr")
                url = "https://catalog.archives.gov/api/v1/?q="+str(query_french)
                self.results_url = "https://catalog.archives.gov/search?q="+str(query_french)
                self.result_search_term = str(query_french)
          except:
              url = "https://catalog.archives.gov/api/v1/?q="+str(query[0])
              self.results_url = "https://catalog.archives.gov/search?q="+query[0]
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
