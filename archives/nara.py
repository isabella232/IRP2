from collection import Collection
import requests
import json

class NARACatalog(Collection):

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        query = "+".join(inputs.split())
        url = "https://catalog.archives.gov/api/v1/?q="+query
        res = requests.get(url)
        parsed = res.json()
        num = parsed["opaResponse"]["results"]["total"]

        self.results_url = "https://catalog.archives.gov/search?q="+query
        if num!= None:
            self.results_count = num
        else:
            self.results_count = 0
        return self
