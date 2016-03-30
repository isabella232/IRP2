from collection import Collection
import requests, json
from textblob import TextBlob

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
        print 'fold3'



        #print 'fold3 : '+ inputs
        #print 'fold3 : '+ self.inputs



        # query = " ".join(inputs.split())
        data = {'engine':'solr'}

        date_clause = ''
        if 'startYear' in inputs and inputs['startYear'].strip() != '':
            date_clause = ',{"type":"date","values":{"name":"year","start":"'+inputs['startYear']+'","end":"'+inputs['endYear']+'","showMissing":false}}'
       # print inputs['general']



        '''
        if 'German' in inputs:
            blob = TextBlob(str(inputs.getlist('general')))
            inputs['general'] = blob.translate(to="de")
            self.result_search_term = inputs['general']
            keywords = inputs['general']+" "+inputs['location']+" "+inputs['artist']
        if 'French' in inputs:
            blob = TextBlob(str(inputs.getlist('general')))
            inputs['general'] = blob.translate(to="fr")
            self.result_search_term = inputs['general']
            keywords = inputs['general']+" "+inputs['location']+" "+inputs['artist']
        '''
        keywords = inputs['general']+" "+inputs['location']+" "+inputs['artist']
        #print 'keywords'
        #print keywords
        try:
         if 'German' in inputs:
            blob = TextBlob(keywords)
            keywords = str(blob.translate(to="de"))
            print keywords
            self.result_search_term = keywords


         elif 'French' in inputs:
            blob = TextBlob(keywords)
            keywords = str(blob.translate(to="fr"))
            print keywords
            self.result_search_term = keywords
        except:
            keywords = inputs['general']+" "+inputs['location']+" "+inputs['artist']
            pass
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
        #print q
        z = json.loads(q)
        #z1 = z["terms"]

        #Translation doesn't work
        # print z1[1]['values']['value']





        data["query_terms"] = q

        url = "http://www.fold3.com/js_getresults.php"
        #print data
        #print data["query_terms"]
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
