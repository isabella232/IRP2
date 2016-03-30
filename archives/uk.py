__author__ = 'anuj'
from collection import Collection
from bs4 import BeautifulSoup 
import requests
import json
from textblob import TextBlob

class UKFindingAid(Collection):

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
                url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+str(query_german)+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
                self.result_search_term = str(query_german)

            elif (query[0]=='French') :
                query_french = blob.translate(to="fr")
                url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+str(query_french)+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
                self.result_search_term = str(query_french)
         except:
            url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+query[0]+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
            pass

        else:
             url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+query[0]+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
             self.result_search_term = str(query[0])


        #url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+query+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        results = soup.find_all("li", class_="tna-result")
        count = results.__len__()

        self.results_url = url
        self.results_count = count

        return self