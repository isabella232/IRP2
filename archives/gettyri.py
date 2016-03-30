__author__ = 'gregjan'
from collection import Collection
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

        query = inputs.split(' ')
        x=len(query)
        print x

        if (x>1):
         try:
            blob = TextBlob(query[1])
            if (query[0]=='German'):
                query_german = blob.translate(to="de")
                url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_german)
                self.results_url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_german)
                self.result_search_term = str(query_german)

            elif (query[0]=='French') :
                query_french = blob.translate(to="fr")
                url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_french)
                self.results_url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query_french)
                self.result_search_term = str(query_french)
         except:
             url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query[0])
             pass
        else:
          url = "http://www.getty.edu/Search/SearchServlet?qt="+str(query[0])
          self.results_url = "http://www.getty.edu/Search/SearchServlet?qt="+query[0]
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
