# -*- coding: utf-8 -*-
from archives.collection import Collection
import requests
import json
import logging
from urllib.parse import quote_plus


class ArdeliaHall(Collection):

    info = {
        'name': 'Fold3 Holocaust Era Assets',
        'class': 'Fold3',
        'lang': 'en',
        'fields': {
            'keywords': 'keyword',
            'startYear': 'start',
            'endYear': 'end'
            }  # NOTE: field mapping done locally for Fold3
        }

    def keywordResultsCount(self, **kwargs):
        keywords = self.add_unsupported_fields_to_keywords(kwargs)
        # NOTE: keywords are escaped by json.dumps
        # keywords = quote_plus(keywords) not needed for JSON
        data = {'engine': 'solr'}
        date_clause = None
        if kwargs['startYear'] is not None and kwargs['endYear'] is not None:
            date_clause = {"type": "date", "values":
                           {"name": "year", "start": kwargs['startYear'], "end": kwargs['endYear'],
                            "showMissing": False}}

        # NOTE: Holocaust Assets return no results for Berlin or Paris, useless field
        # location_clause = ''
        # if 'location' in inputs and inputs['location'].strip() != '':
        # location_clause =
        # ',{"type":"field","values":{"name":"place","value":"'+inputs['location']+'"}}'

        # NOTE: category 114 is "Holocaust Collection"
        q = {"terms":
             [
              {"type": "category", "values": {"value": 114}},
              {"type": "keyword", "values": {"value": keywords}}
             ],
             'index': 0
             }
        if date_clause is not None:
            q['terms'].append(date_clause)
        data["query_terms"] = json.dumps(q)
        url = "http://www.fold3.com/js_getresults.php"
        res = requests.post(url, params=data)
        parsed = res.json()
        num = 0
        try:
            num = parsed["recCount"]
        except:
            logging.debug("Fold3 returned:\n{0}".format(json.dumps(parsed)))

        self.results_url = "http://www.fold3.com/s.php#cat=114&query={0}" \
                           .format(quote_plus(keywords))
        if kwargs['startYear'] is not None and kwargs['endYear'] is not None:
            self.results_url += "&dr_year={0}&dr_year2={1}" \
                                .format(kwargs['startYear'], kwargs['endYear'])
        if num is not None:
            self.results_count = num
        else:
            self.results_count = 0
        return self


# {"terms":[{"type":"date","values":{"name":"year","start":"1945","end":"1946","showMissing":true}},{"type":"ocr","values":{"value":"true"}},{"type":"category","values":{"value":115}}],"index":0}
