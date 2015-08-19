from collection import Collection
import requests

class Fold3(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = " ".join(inputs.split())
        data = {'engine':'solr'}
        data["query_terms"] = '{"terms":[{"type":"category","values":{"value":114}},{"type":"keyword","values":{"value":"'+query+'"}}],"index":0}'
        url = "http://www.fold3.com/js_getbasicfacets.php"
        res = requests.post(url, data=data)
        parsed = res.json()
        num = parsed["recCount"]

        self.results_url = "http://www.fold3.com/s.php#cat=114&query="+query
        if num!= None:
            self.results_count = num
        else:
            self.results_count = 0
        return self
