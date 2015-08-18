import collections
import requests

class Fold3(collections.Collection):
    collection_info_url = 'fold3.com'
    logo_file = 'logo-nara.png'
    inst_key = 'nara'
    fullname = 'Fold3 Holocaust Era Assets'
    researcher_hints = ''
    description_lang = 'en'

    def keywordResultsCount(self, inputs):
        query = " ".join(inputs.split())
        data = {'engine':'solr'}
        data["query_terms"] = '{"terms":[{"type":"category","values":{"value":114}},{"type":"keyword","values":{"value":"'+query+'"}}],"index":0}'
        url = "http://www.fold3.com/js_getbasicfacets.php"
        res = requests.post(url, data=data)
        parsed = res.json()
        num = parsed["recCount"]

        result = {}
        result["url"] = "http://www.fold3.com/s.php#cat=114&query="+query
        if num!= None:
            result["count"] = num
        else:
            result["count"] = 0

        return result
