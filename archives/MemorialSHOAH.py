# -*- coding: utf-8 -*-
from archives.collection import Collection
import requests
from requests.adapters import HTTPAdapter
import logging
from bs4 import BeautifulSoup
# from urllib.parse import quote_plus


class MemorialSHOAH(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs, join_with=' OR ')
        # keywords = quote_plus(keywords)

        url = "http://bdi.memorialdelashoah.org/internet/jsp/core/MmsGlobalSearch.jsp"

        self.results_url = url
        self.results_count = 0
        try:
            with requests.Session() as s:
                s.mount('http://bdi.memorialdelashoah.org/internet/jsp/core/MmsGlobalSearch.jsp',
                        HTTPAdapter(max_retries=0))
                f = s.get('http://bdi.memorialdelashoah.org/internet/jsp/core/MmsGlobalSearch.jsp',
                          timeout=10).text
                fsoup = BeautifulSoup(f, "lxml")
                keywordsInputName = fsoup.find('input', {'id': 'texteRecherche'})['name']
                actionInputName = fsoup.find('input', {'id': 'defaultAction'})['name']
                keywordsInputName = fsoup.find('input', {'id': 'texteRecherche'})['name']
                data = {
                    keywordsInputName: keywords,
                    actionInputName: "Rechercher"
                }
                html = s.post(url, data=data, timeout=15).text
                soup = BeautifulSoup(html, "lxml")
            div = soup.find("div", {'id': "searchBarResult"})
            responseText = div.h3.span.string
            self.results_count = int(responseText.split()[4])
        except Exception as e:
            logging.exception(e)
            self.message = "Timeout error. Please try again later."
            pass
        return self
