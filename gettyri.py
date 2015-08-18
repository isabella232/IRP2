__author__ = 'gregjan'
import collections
from bs4 import BeautifulSoup
import urllib2

class GettyRI(collections.Collection):
    collection_info_url = 'http://www.getty.edu/museum/research/provenance/index.html'
    logo_file = 'getty.jpg'
    inst_key = 'getty'
    fullname = 'Getty Research Institute'
    researcher_hints = ''
    description_lang = 'en'

def keywordResultsCount(self, inputs):
    query = "+".join(inputs.split())
    url = "http://www.getty.edu/Search/SearchServlet?qt="+query
    res = urllib2.urlopen(url)
    html = res.read()
    soup = BeautifulSoup(html, "lxml")

    table = soup.find_all("table")[2]
    num = table.find("td").contents[0].strip().split()
    count = num[1]

    self.url = url
    if (count.isdigit()):
         self.count = count
    else:
         self.count = 0

    return self
