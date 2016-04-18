# -*- coding: utf-8 -*-
from archives.collection import Collection
import requests
from urllib.parse import quote_plus


class NARACatalog(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs)
        keywords = quote_plus(keywords)

        url = "https://catalog.archives.gov/api/v1/?q={0}".format(keywords)
        self.results_url = "https://catalog.archives.gov/search?q={0}".format(keywords)

        res = requests.get(url)
        parsed = res.json()
        num = parsed["opaResponse"]["results"]["total"]

        # self.results_url = "https://catalog.archives.gov/search?q="+query
        if num is not None:
            self.results_count = num
        else:
            self.results_count = 0
        return self
