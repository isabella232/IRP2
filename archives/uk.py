# -*- coding: utf-8 -*-
from archives.collection import Collection
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote_plus


class UKFindingAid(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs, join_with=' OR ')
        keywords = quote_plus(keywords)

        url = "http://discovery.nationalarchives.gov.uk/results/r?_q={0}" \
              "&_sd=&_ed=&discoveryCustomSearch=true&_col=200&_dt=LA&_hb=tna" \
              .format(keywords)

        self.results_url = url
        self.results_count = 0
        try:
            html = requests.get(url, timeout=8).text
            soup = BeautifulSoup(html, "lxml")
            recordstxt = soup.find("li", {'id': "records-tab"}).span.string
            logging.debug("got result: ".format(recordstxt))
            self.results_count = int(recordstxt.split(' ')[1])
        except Exception as e:
            logging.exception(e)
            self.message = "Timeout error. Please try again later."
            pass
        return self
