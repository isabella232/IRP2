from collection import Collection
import requests, json

class Fold3(Collection):

    info = {
        'name': 'Fold3 Holocaust Era Assets',
        'class': 'Fold3',
        'lang': 'en',
        'fields': {
            'general': 'keyword',
            'startYear': 'start',
            'endYear': 'end'
        } # NOTE: field mapping done locally for Fold3
    }

    def keywordResultsCount(self, inputs):
        self.inputs = inputs['general']
        # query = " ".join(inputs.split())
        data = {'engine':'solr'}

        date_clause = ''
        if 'startYear' in inputs and inputs['startYear'].strip() != '':
            date_clause = ',{"type":"date","values":{"name":"year","start":"'+inputs['startYear']+'","end":"'+inputs['endYear']+'","showMissing":false}}'

        keywords = inputs['general']+" "+inputs['location']+" "+inputs['artist']
        # NOTE: Holocaust Assets return no results for Berlin or Paris, useless field
        # location_clause = ''
        # if 'location' in inputs and inputs['location'].strip() != '':
        #     location_clause = ',{"type":"field","values":{"name":"place","value":"'+inputs['location']+'"}}'

        # NOTE: category 114 is "Holocaust Collection"
        q = ('{"terms":['
        '{"type":"category","values":{"value":114}},'
        '{"type":"keyword","values":{"value":"'+ keywords +'"}}')
        q += date_clause
        #q += location_clause
        q += '],"index":0}'
        json.loads(q)
        data["query_terms"] = q
        url = "http://www.fold3.com/js_getresults.php"
        res = requests.post(url, params=data)
        parsed = res.json()
        num = parsed["recCount"]

        self.results_url = "http://www.fold3.com/s.php#cat=114&query="+keywords.replace(' ','+')
        if 'startYear' in inputs and inputs['startYear'].strip() != '':
            self.results_url += "&dr_year="+inputs['startYear']+"&dr_year2="+inputs['endYear']
        if num!= None:
            self.results_count = num
        else:
            self.results_count = 0
        return self



# {"terms":[{"type":"date","values":{"name":"year","start":"1945","end":"1946","showMissing":true}},{"type":"ocr","values":{"value":"true"}},{"type":"category","values":{"value":115}}],"index":0}
