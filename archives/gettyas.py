__author__ = 'gregjan'
from collection import Collection
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

class GettyAS(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        #query = " ".join(inputs.split())
        query = inputs.split(' ')
        x=len(query)



        session = requests.session()
        r = session.get("http://piprod.getty.edu/starweb/pi/servlet.starweb?path=pi/pi.web#?")
        # obtain input values for __websessionID and __sessionNumber
        soup = BeautifulSoup(r.text, "lxml")

        # Result number
        #websessionID = soup.find_all("input",name="__websessionID")[0].value
        #sessionNumber = soup.find_all("input",name="__sessionNumber")[0].value
        websessionID = soup.select('input[name="__websessionID"]')[0]['value']
        sessionNumber = soup.select('input[name="__sessionNumber"]')[0]['value']

        data = {}
        data['__websessionID'] = websessionID
        data['__sessionNumber'] = str(sessionNumber)
        data['__pageid'] = 'SalesCatSearch'
        data['__hiddenstyle'] = 'A'
        data['__numberstyle'] = 'A'
        data['__dirtyFlag'] = 'Clean'
        data['__action'] = '611'
        data['Keywords'] = query
        data['Operators'] = 'AND'
        data['NameType'] = 'BUYER%2CSELLER'
        data['__jsModel'] = 'New'

        url = "http://piprod.getty.edu/starweb/pi/servlet.starweb"
        r = session.post(url, data=data)
        #print 'gettyas:'+ str(data['Keywords'])
        soup = BeautifulSoup(r.text, "lxml")

        #Sale Catalog Contents:  69 results from
        # <span class="hitcount" name="DatabaseSearched" starweb_type="Conditional">
        # 69
        # </span> records retrieved
        spanList = soup.select('span[name="DatabaseSearched"]')
        num = None
        if len(spanList)>0:
            numTxt = spanList[0].string
            num = int(numTxt)
        if (x>1)  :
         self.result_search_term = query[1]
        else:
          self.result_search_term = query[0]

        self.results_url = "http://piprod.getty.edu/starweb/pi/servlet.starweb?path=pi/pi.web"
        if num!= None:
            self.results_count = num
        else:
            self.results_count = 0
        return self
