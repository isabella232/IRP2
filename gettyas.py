__author__ = 'gregjan'
import collections
from bs4 import BeautifulSoup
import requests

class GettyAS(collections.Collection):
    collection_info_url = 'http://www.getty.edu/museum/research/provenance/index.html'
    logo_file = 'getty.jpg'
    inst_key = 'getty'
    fullname = 'Getty German Art Sales Catalogs'
    researcher_hints = ''
    description_lang = 'en'

def keywordResultsCount(self, inputs):
    # parse query and fetch html result
    query = " ".join(inputs.split())
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

    # pack the result
    result = {}
    result["url"] = "http://piprod.getty.edu/starweb/pi/servlet.starweb?path=pi/pi.web"
    if num != None:
        result["count"] = num
    else:
        result["count"] = 0

    return result
