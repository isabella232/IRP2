# -*- coding: utf-8 -*-
__author__ = 'anuj'
from archives.collection import Collection
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

class UKFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        #query = "+".join(inputs.split())

        query = inputs.split(' ',1)
        x=len(query)
        print x

        if (x>1):

         try:
            blob = TextBlob(query[1])
            print 'uk try'
            if (query[0]=='German'):
              try:
                query_german = blob.translate(to="de")
                print query_german
                #query_german = unicode( query_german, "utf-8" )
                url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+str(query_german)+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
                self.result_search_term = str(query_german)
                #self.result_search_term = self.result_search_term.encode('utf-8')
              except:
                query_german = blob.translate(to="de")
                query_german = unicode( query_german, "utf-8" )
                url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+str(query_german)+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
                self.result_search_term = str(query_german)
                self.result_search_term = self.result_search_term.encode('utf-8')


            elif (query[0]=='French') :
              try:
                query_french = blob.translate(to="fr")
                #query_french = unicode( query_french, "utf-8" )
                url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+str(query_french)+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
                self.result_search_term = str(query_french)
                #self.result_search_term = self.result_search_term.encode('utf-8')
              except:
                query_french = blob.translate(to="fr")
                query_french = unicode( query_french, "utf-8" )
                url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+str(query_french)+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
                self.result_search_term = str(query_french)
                self.result_search_term = self.result_search_term.encode('utf-8')

            else:
                query1 = " "+ inputs
                query1 = query1.split(' ',1)
                url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+query1[1]+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
                self.result_search_term = str(query1[1])

        except Exception as e:
            url = "http://discovery.nationalarchives.gov.uk/results/r?_q="+query[1]+"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
            self.result_search_term = str(query[1])
            print 'uk'
            print str(e)
            pass

        else:
            url = "http://discovery.nationalarchives.gov.uk/results/r?_q="
            +query[0]
            +"&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna"
            self.result_search_term = str(query[0])

        try:
            html = requests.get(url, timeout=8).text
            soup = BeautifulSoup(html, "lxml")
            results = soup.find_all("li", class_="tna-result")
            count = results.__len__()
        except:
            url = "https://www.google.com/webhp?hl=en"
            html = requests.get(url).text
            print("Timeout error. Please try again later.")
            pass

        soup = BeautifulSoup(html, "lxml")


        self.results_url = url
        self.results_count = count

        return self
