__author__ = 'Anuj'
from collection import Collection
from bs4 import BeautifulSoup
import requests
import re
import json
import goslate
from textblob import TextBlob


class BerlinFindingAid(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs

        print self.inputs
        print inputs

        query = inputs.split(' ')
        x=len(query)
        print x
        #print query[1]

        '''
        gs = goslate.Goslate()
        query1=gs.translate(query[2], 'de')
        print query1
        '''

        if (x>1):
         try:
            blob = TextBlob(query[1])
            if (query[0]=='German'):
                query_german = blob.translate(to="de")
                self.result_search_term = str(query_german)
                url = "http://www.lostart.de/Webs/DE/Datenbank/SucheMeldungSimpel.html?resourceId=4424&input_=4046&pageLocale=de&simpel="+str(query_german)+"&type=Simpel&type.HASH=a367122406f8d243ac08&suche_typ=MeldungSimpel&suche_typ.HASH=e2ace3636225271222d5&suchen=Suchen"
            elif (query[0]=='French') :
                query_french = blob.translate(to="fr")
                self.result_search_term = str(query_french)
                url = "http://www.lostart.de/Webs/DE/Datenbank/SucheMeldungSimpel.html?resourceId=4424&input_=4046&pageLocale=de&simpel="+str(query_french)+"&type=Simpel&type.HASH=a367122406f8d243ac08&suche_typ=MeldungSimpel&suche_typ.HASH=e2ace3636225271222d5&suchen=Suchen"
         except:
            url = "http://www.lostart.de/Webs/DE/Datenbank/SucheMeldungSimpel.html?resourceId=4424&input_=4046&pageLocale=de&simpel="+query[0]+"&type=Simpel&type.HASH=a367122406f8d243ac08&suche_typ=MeldungSimpel&suche_typ.HASH=e2ace3636225271222d5&suchen=Suchen"
            pass

        else:
            url = "http://www.lostart.de/Webs/DE/Datenbank/SucheMeldungSimpel.html?resourceId=4424&input_=4046&pageLocale=de&simpel="+query[0]+"&type=Simpel&type.HASH=a367122406f8d243ac08&suche_typ=MeldungSimpel&suche_typ.HASH=e2ace3636225271222d5&suchen=Suchen"
            self.result_search_term = str(query[0])

        #query = "+".join(inputs.split())

        #url_g = "http://www.lostart.de/Webs/DE/Datenbank/SucheMeldungSimpel.html?resourceId=4424&input_=4046&pageLocale=de&simpel="+str(query_german)+"&type=Simpel&type.HASH=a367122406f8d243ac08&suche_typ=MeldungSimpel&suche_typ.HASH=e2ace3636225271222d5&suchen=Suchen"
        #url_f = "http://www.lostart.de/Webs/DE/Datenbank/SucheMeldungSimpel.html?resourceId=4424&input_=4046&pageLocale=de&simpel="+str(query_french)+"&type=Simpel&type.HASH=a367122406f8d243ac08&suche_typ=MeldungSimpel&suche_typ.HASH=e2ace3636225271222d5&suchen=Suchen"



        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        #divs = soup.find_all('div')
        #print "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBb"
        #results = soup.find("div", {"id" : "id67734"})
        #results_1 = results.find("table", {"summary" : "suche0"})
        #results_2 = results_1.find("tbody")
        #results_3 = results_2.find_all("tr")
        #count =  results_3.__len__()

        results = soup.find("div", {"id" : "id67734"})
        results_1 = results.find("table", {"summary" : "suche0"})


        if results_1 is not None:
            captionResults = results_1.find("caption")
            #print 'berlin_captionResults : ' + str(captionResults)
            string1 = captionResults.string
            #print 'berlin_string1 : ' + str(string1)
            self.results_count = int(string1.split()[0])
        else:
            self.results_count = 0

        self.results_url = url


        return self
