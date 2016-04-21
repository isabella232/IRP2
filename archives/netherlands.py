# -*- coding: utf-8 -*-
from archives.collection import Collection
from bs4 import BeautifulSoup
import requests
import logging
from urllib.parse import quote_plus


class NetherlandsFindingAid(Collection):


    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs)
        keywords = quote_plus(keywords)
        url = "http://www.archieven.nl/nl/zoeken?" \
              "mizig=0&miview=lst&milang=nl&micols=1&mires=0&mizk_of={0}" \
              .format(keywords)
        logging.debug("NL URL:\n{0}".format(url))
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        spanList = soup.select('span.mi_hits_hits_count')
        num = 0
        s = spanList[0].string
        try:
            num = int(s)
        except:
            pass
        self.results_url = url
        self.results_count = num
        return self
