# -*- coding: utf-8 -*-
from archives.collection import Collection
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus


class GettyRI(Collection):
    results_count = None
    results_url = None
    result_search_term = None
    inputs = None

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs)
        keywords = quote_plus(keywords)

        url = "http://www.getty.edu/Search/SearchServlet?qt={0}".format(keywords)
        self.results_url = url

        # url = "http://www.getty.edu/Search/SearchServlet?qt="+query
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        table = soup.find_all("table")[2]
        num = table.find("td").contents[0].strip().split()
        count = num[1]

        # self.results_url = url
        if (count.isdigit()):
            self.results_count = count
        else:
            self.results_count = 0
        return self
