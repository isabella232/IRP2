class Collection(object):
    results_count = None
    results_url = None
    inputs = None
    result_search_term = None
    def emit(self):
        result = {
            'class': type(self).__name__,
            'results_count': self.results_count,
            'results_url': self.results_url,
            'inputs': self.inputs,
            'result_search_term': self.result_search_term
        }
        return result

    def keywordResultsCount(self, inputs):
        # Performs a keyword query on the collections and counts the results.
        # Results are stored in instance variables.
        # Returns self.
        pass

    def mapParameters(self, inputs):
        # Creates a dictionary of parameters for a collection search.
        # Can be used for POST or GET requests as appropriate.
        # Uses self.info['fields'], which is a dict that maps the keys in our inputs
        # to the parameter names in a collection search form.
        result = {}
        fields = self.info['fields']
        for key in inputs:
            if key in fields:
                result[fields[key]] = inputs[key]
        return result
