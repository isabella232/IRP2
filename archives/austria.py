from archives.collection import Collection
from bs4 import BeautifulSoup
import requests


class AustriaFindingAid(Collection):

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs)
        session = requests.session()
        data = {}
        data['search'] = keywords
        data['FORM_SUBMIT'] = "adb_construct_en"
        data['FORM_DATA'] = "date"
        data['selfsend'] = "1"
        data['page'] = "1"
        data['orderby'] = "1"
        data['perPage'] = "20"
        url = "http://www.kunstrestitution.at/catalogue_detailsearch.html"
        r = session.post(url, data=data)
        soup = BeautifulSoup(r.text, "lxml")

        num = None
        spanList = soup.select('span.total')
        s = spanList[0].string
        newString = s[s.find("(") + 1:s.find(")")]
        if len(newString) > 0:
            num = int(newString)

        self.results_url = url

        if num is not None:
            self.results_count = num
        else:
            self.results_count = 0

        return self
