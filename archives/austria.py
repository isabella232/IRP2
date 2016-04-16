__author__ = 'anuj'
from archives.collection import Collection
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

class AustriaFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        session = requests.session()
        data = {}
        z = []
        data['search'] = inputs
        data['search'] = data['search'].split(' ', 1)
        x = len(data['search'])

        if (x > 1):
        #Translate to Dutch
         try:
           if(data['search'][0]=='German') :
             blob = TextBlob(data['search'][1])
             data['search'] = str(blob.translate(to="de"))
             self.result_search_term = str(data['search'])

           elif (data['search'][0]=='French') :
             blob = TextBlob(data['search'][1])
             data['search'] = str(blob.translate(to="fr"))
             self.result_search_term = str(data['search'])
           else:
               data['search']= " "+inputs
               data['search'] = data['search'].split(' ',1)
               data['search']=str(data['search'][1])
               self.result_search_term = str(data['search'][1])

         except:
             self.result_search_term = str(data['search'][1])
             pass
        else:
            data['search']=str(data['search'][0])
        url = "http://www.kunstrestitution.at/catalogue_detailsearch.html"

        '''
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        '''

        r = session.post(url, data=data)
        soup = BeautifulSoup(r.text, "lxml")
        spanList = soup.select('span.total')
        num = None
        s = spanList[0].string

        newString = s[s.find("(")+1:s.find(")")]

        if len(newString) > 0:
            num = int(newString)

        self.results_url = url

        if num is not None:
            self.results_count = num
        else:
            self.results_count = 0

        return self
