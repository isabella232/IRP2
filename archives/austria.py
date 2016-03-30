__author__ = 'anuj'
from collection import Collection
from bs4 import BeautifulSoup 
import requests
import json
import goslate
from textblob import TextBlob

class AustriaFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        session = requests.session()
        data = {}
        z = []
        data['search'] = inputs
        print 'austria'
        #print data['search'].split(' ')

        data['search'] = data['search'].split(' ')
        print data['search'][0]

        x = len(data['search'])

        if (x>1):
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
        #print (gs.translate(data['search'], 'de'))
         except:
             pass
        else:
            data['search']=str(data['search'][0])
            print 'data (no translation): ' + str(data)
            print data
        url = "http://www.kunstrestitution.at/catalogue_detailsearch.html"

        '''
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        '''

        r = session.post(url,data = data)
        soup = BeautifulSoup(r.text, "lxml")

        #print soup

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
