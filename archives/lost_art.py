# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.request import urlopen
import logging

from bs4 import BeautifulSoup

from archives.collection import Collection


# TODO: switch to site's adv search
# TODO: use "mattech" parameter for technique
# TODO: person = artist
# TODO: ort = place

class LostArt(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs, join_with=' ')
        url = "http://www.lostart.de/Webs/EN/LostArt/Service/GlobalSuche/ServiceSuche.html"
        params = dict(
            pageLocale="en",
            templateQueryString=keywords,
            suche_typ="Global",
            submit="Search"
        )

        # For extremely weird reasons I don't understand, the requests library
        # returns a 403 response. Maybe it's to do with the charset encoding or
        # something (???). Anyway, urlopen seems to work and return data...
        self.results_url = url + "?" + urlencode(params)
        self.results_count = 0
        with urlopen(self.results_url) as response:
            data = response.read()
            soup = BeautifulSoup(data, "lxml")
            tag = soup.select_one(".resultLinks")

            if tag is not None:
                try:
                    self.results_count = int(tag.text.split()[0])
                except Exception as e:
                    logging.exception(e)

        return self
