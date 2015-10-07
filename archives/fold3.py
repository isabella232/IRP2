from collection import Collection
import requests, json

class Fold3(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = " ".join(inputs.split())
        data = {'engine':'solr'}
        q = '{"terms":[{"type":"category","values":{"value":114}},{"type":"keyword","values":{"value":"'+query+'"}}],"index":0}'
        data["query_terms"] = q
        url = "http://www.fold3.com/js_getresults.php"
        res = requests.get(url, params=data)
        parsed = res.json()
        num = parsed["recCount"]

        self.results_url = "http://www.fold3.com/s.php#cat=114&query="+query
        if num!= None:
            self.results_count = num
        else:
            self.results_count = 0
        return self
