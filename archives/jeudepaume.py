from archives.collection import Collection
from bs4 import BeautifulSoup
import requests


class JeuDePaume(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs)

        # obtain session values for __websessionID and __sessionNumber
        session = requests.session()
        r = session.get("http://piprod.getty.edu/starweb/pi/servlet.starweb?path=pi/pi.web#?")
        soup = BeautifulSoup(r.text, "lxml")
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
        data['Keywords'] = keywords
        data['Operators'] = 'OR'
        data['NameType'] = 'BUYER%2CSELLER'
        data['__jsModel'] = 'New'

        url = "http://piprod.getty.edu/starweb/pi/servlet.starweb"
        r = session.post(url, data=data)
        soup = BeautifulSoup(r.text, "lxml")

        # Sale Catalog Contents:  69 results from
        # <span class="hitcount" name="DatabaseSearched" starweb_type="Conditional">
        # 69
        # </span> records retrieved
        spanList = soup.select('span[name="DatabaseSearched"]')
        num = None
        if len(spanList) > 0:
            numTxt = spanList[0].string
            num = int(numTxt)

        self.results_url = "http://piprod.getty.edu/starweb/pi/servlet.starweb?path=pi/pi.web"
        if num is not None:
            self.results_count = num
        else:
            self.results_count = 0
        return self
