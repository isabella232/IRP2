import collections
import requests
import json

class NARACatalog(collections.Collection):
    collection_info_url = 'http://www.archives.gov/research/'
    logo_file = 'logo-nara.png'
    inst_key = 'nara'
    fullname = 'US National Archives and Records Administration'
    researcher_hints = ''
    description_lang = 'en'

    def keywordResultsCount(self, inputs):
        # parse query and fetch html result
        query = "+".join(inputs.split())
        # TODO: advanced search support
        url = "https://catalog.archives.gov/api/v1/?q="+query
        res = requests.get(url)
        parsed = res.json()
        num = parsed["opaResponse"]["results"]["total"]

        # pack the result
        result = {}
        result["url"] = "http://search.archives.gov/query.html?qt="+query
        if num!= None:
            result["count"] = num
        else:
            result["count"] = 0

        return result
