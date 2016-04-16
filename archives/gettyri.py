# -*- coding: utf-8 -*-
__author__ = 'gregjan'
from archives.collection import Collection
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

class GettyRI(Collection):
    results_count = None
    results_url = None
    result_search_term = None
    inputs = None

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        #query = "+".join(inputs.split())

        query = inputs.split(' ',1)
        x=len(query)


        if (x>1):

         try:
            blob = TextBlob(query[1])
            if (query[0]=='German'):
             try :
                query_german = blob.translate(to="de")
                #query_german = unicode( query_german, "utf-8" )
                url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_german)

                self.results_url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_german)
                self.result_search_term = str(query_german)
                #self.result_search_term = self.result_search_term.encode('utf-8')
             except:
                query_german = blob.translate(to="de")
                query_german = unicode( query_german, "utf-8" )
                url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_german)

                self.results_url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_german)
                self.result_search_term = str(query_german)
                self.result_search_term = self.result_search_term.encode('utf-8')


            elif (query[0]=='French') :
             try:
                query_french = blob.translate(to="fr")
                #query_french = unicode( query_french, "utf-8" )
                url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_french)
                self.results_url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_french)
                self.result_search_term = str(query_french)
                #self.result_search_term = self.result_search_term.encode('utf-8')
             except:
                query_french = blob.translate(to="fr")
                query_french = unicode( query_french, "utf-8" )
                url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_french)
                self.results_url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_french)
                self.result_search_term = str(query_french)
                self.result_search_term = self.result_search_term.encode('utf-8')

            else:
                query1 = " "+inputs
                query1 = query1.split(' ',1)
                url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query1[1])
                self.result_search_term = str(query1[1])

         except:
             #query1 = " "+inputs
             #query1 = query1.split(' ',1)
             url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query[1])
             self.result_search_term = str(query[1])
             pass
        else:
          url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query[0])
          self.results_url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query[0])
          self.result_search_term = str(query[0])

        #url = "http://www.getty.edu/Search/SearchServlet?qt="+query
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        table = soup.find_all("table")[2]
        num = table.find("td").contents[0].strip().split()
        count = num[1]

       # self.results_url = url
        if (count.isdigit()):
             self.results_count = count
        else:
             self.results_count = 0
        return self
