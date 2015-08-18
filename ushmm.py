import collections
import urllib2
from bs4 import BeautifulSoup

class USHMM(collections.Collection):
    collection_info_url = 'http://www.ushmm.org/research/research-in-collections/overview'
    logo_file = 'logo-ushmm.png'
    inst_key = 'ushmm'
    fullname = 'United States Holocaust Memorial Museum'
    researcher_hints = ''
    description_lang = 'en'

    def keywordResultsCount(self, inputs):
        # parse query and fetch html result
        query = "+".join(inputs.split())
        # TODO: advanced search support
        url = "http://www.errproject.org/jeudepaume/card_search.php?Query=" + query
        res = urllib2.urlopen(url)
        html = res.read()
        soup = BeautifulSoup(html, "lxml")

        # Result number
        num = soup.find("div",class_="num")
        if num!= None:
            counts = num.contents[0]
            count = counts.split()[5]
        else:
            count = 0

        # pack the result
        result = {}
        result["url"] = url
        result["count"] = count

        return result
