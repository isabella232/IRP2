# -*- coding: utf-8 -*-
from archives.collection import Collection
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

class USHMM(Collection):

    info = {
        'name': 'Jeu de Paume',
        'class': 'USHMM',
        'lang': 'en',
        'fields': {
            'general': 'Solr__Query',
            'artist': 'Solr__Artist',
            'location': 'Solr__ObjectPostConfiscationHistory',
            'German': 'German',
            'French': 'French'
        }
    }

    def keywordResultsCount(self, inputs):
        self.inputs = inputs['general']
        params = self.mapParameters(inputs)

        print 'ushmm'
        print params

        try:

         if 'German'in params:
          try:
            g = params['Solr__Query']
            z1 = str(g)
            blob = TextBlob(z1)
            params['Solr__Query']=str(blob.translate(to="de"))
            #params['Solr__Query'] = unicode( params['Solr__Query'], "utf-8" )
            print params
            self.result_search_term = params['Solr__Query']
            #self.result_search_term = self.result_search_term.encode('utf-8')
            print self.result_search_term
          except:
            g = params['Solr__Query']
            z1 = str(g)
            blob = TextBlob(z1)
            params['Solr__Query']=str(blob.translate(to="de"))
            params['Solr__Query'] = unicode( params['Solr__Query'], "utf-8" )
            print params
            self.result_search_term = params['Solr__Query']
            self.result_search_term = self.result_search_term.encode('utf-8')
            print self.result_search_term


         if 'French' in params:
          try:
            g = params['Solr__Query']
            z1 = str(g)
            blob = TextBlob(z1)
            params['Solr__Query']=str(blob.translate(to="fr"))
            #params['Solr__Query'] = unicode( params['Solr__Query'], "utf-8" )
            print params
            self.result_search_term = params['Solr__Query']
            #self.result_search_term = self.result_search_term.encode('utf-8')
            print self.result_search_term
          except:
            g = params['Solr__Query']
            z1 = str(g)
            blob = TextBlob(z1)
            params['Solr__Query']=str(blob.translate(to="fr"))
            params['Solr__Query'] = unicode( params['Solr__Query'], "utf-8" )
            print params
            self.result_search_term = params['Solr__Query']
            self.result_search_term = self.result_search_term.encode('utf-8')
            print self.result_search_term

        except:
            self.result_search_term = params['Solr__Query']
            pass
        '''
        query = inputs['general'].split(' ')
        x=len(query)
        '''
        url = "http://www.errproject.org/jeudepaume/card_advanced_search.php"
        r = requests.get(url, params=params)
        html = r.text
        soup = BeautifulSoup(html, "lxml")

        results = soup.find_all("tr", class_="results")
        count = results.__len__()
        '''
        if (x>1):
            self.result_search_term = query[1]
        else:
            self.result_search_term = query[0]
        '''
        #self.result_search_term = 'none'
        self.results_url = r.url
        self.results_count = count

        return self
