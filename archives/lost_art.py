# -*- coding: utf-8 -*-
from archives.collection import Collection
from bs4 import BeautifulSoup
import requests
import re
import json
from urllib.parse import quote_plus


class LostArt(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs, join_with=' ', term_suffix='~')
        keywords = quote_plus(keywords)

        url = "http://www.lostart.de/Webs/DE/Datenbank/SucheMeldungSimpel.html?" \
              "resourceId=4424&input_=4046&pageLocale=de&simpel={0}" \
              "&type=Simpel&type.HASH=a367122406f8d243ac08&suche_typ=MeldungSimpel" \
              "&suche_typ.HASH=e2ace3636225271222d5&suchen=Suchen" \
              .format(keywords)

        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")

        results = soup.find("div", {"id": "id67734"})
        results_1 = results.find("table", {"summary": "suche0"})

        if results_1 is not None:
            captionResults = results_1.find("caption")
            string1 = captionResults.string
            try:
                self.results_count = int(string1.split()[0])
            except Exception:
                self.results_count = 0
        else:
            self.results_count = 0

        self.results_url = url
        return self
