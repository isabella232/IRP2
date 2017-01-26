# -*- coding: utf-8 -*-
from archives.collection import Collection
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import quote_plus


class DHMMunich(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs, join_with=' OR ')
        keywords = quote_plus(keywords)

        url = ('http://www.dhm.de/datenbank/ccp/dhm_ccp.php?'
               'seite=6'
               '&is_fulltext=true'
               '&fulltext={0}'
               '&suchen=Quick+search'
               '&modus=exakt').format(keywords)

        self.results_url = url
        self.results_count = 0
        try:
            html = requests.get(url, timeout=10).text
            soup = BeautifulSoup(html, "lxml")
            recordstxt = soup.find("h2", {'class': "results"}).string
            logging.debug("got result: ".format(recordstxt))
            self.results_count = int(recordstxt.split(':')[1])
        except Exception as e:
            logging.exception(e)
            self.message = "Timeout error. Please try again later."
            pass
        return self
