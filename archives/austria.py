from archives.collection import Collection
from bs4 import BeautifulSoup
import requests
import logging
from urllib.parse import quote_plus

class AustriaArtDB(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = quote_plus(self.add_unsupported_fields_to_keywords(kwargs))
        url = "https://www.kunstdatenbank.at/search-for-objects/fulltext/{0}".format(keywords)
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        try:
            self.results_url = url
            self.results_count = 0
            tag = soup.select_one('.total strong')
            if tag:
                try:
                    self.results_count = int(tag.text)
                except ValueError:
                    pass
        except Exception as e:
            logging.exception(e)
            self.message = "Timeout error. Please try again later."
            pass
        return self

class FindBuch(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = quote_plus(self.add_unsupported_fields_to_keywords(kwargs))
        url = "https://www.findbuch.at/findbuch-search/searchterm/{0}".format(keywords)
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        try:
            self.results_url = url
            self.results_count = 0
            tag = soup.select_one('#findbuch-search .ce_metamodel_list p strong')
            if tag:
                try:
                    self.results_count = int(tag.text.split()[0])
                except (ValueError, IndexError):
                    pass
        except Exception as e:
            logging.exception(e)
            self.message = "Timeout error. Please try again later."
        return self


