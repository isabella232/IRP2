# -*- coding: utf-8 -*-
from archives.collection import Collection
import requests
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

        q = {
            "ocr": True,
            "filters": [
                {
                    "type": "general.title.category",
                    "values": [114], # Holocaust collection,
                    "exclude": False,
                    "strict": True,
                }
            ],
            "keywords": keywords,
            "maxCount": 0, # Don't need actual results, only count
            "strictMode": "TRUE"
        }
        url = "https://www.fold3.com/search-api/doc-search"
        headers = {"Content-type": "application/json", "Accepts": "application/json"}
        self.results_count = 0
        self.results_url = "https://www.fold3.com/search?general.title.category=114&keywords={0}" \
            .format(quote_plus(keywords))
        try:
            res = requests.post(url, json=q, headers=headers)
            parsed = res.json()
            if parsed.get("total"):
                self.results_count = parsed["total"]
        except Exception as e:
            logging.exception(e)

        return self

