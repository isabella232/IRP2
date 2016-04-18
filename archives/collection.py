class Collection(object):
    results_count = None
    results_url = None
    result_search_term = None
    message = None

    def emit(self):
        result = {
            'class': type(self).__name__,
            'results_count': self.results_count,
            'results_url': self.results_url,
            'message': self.message
        }
        return result

    def keywordResultsCount(self, **kwargs):
        # Performs a keyword query on the collections and counts the results.
        # Results are stored in instance variables.
        # Returns self.
        pass

    def mapParameters(self, inputs, join_with=' '):
        # Creates a dictionary of parameters for a collection search.
        # Can be used for POST or GET requests as appropriate.
        # Uses self.info['fields'], which is a dict that maps the keys in our inputs
        # to the parameter names in a collection search form.
        result = {}
        fields = self.info['fields']
        for key in inputs:
            if key in fields:
                if 'keywords' == key:
                    result[fields[key]] = \
                        self.add_unsupported_fields_to_keywords(inputs, join_with=join_with)
                else:
                    result[fields[key]] = inputs[key]
        return result

    def add_unsupported_fields_to_keywords(self, inputs, join_with=' '):
        """Returns a string that expands keywords with fields not otherwise mapped"""
        result = inputs.get('keywords', '')
        fields = {'keywords': 'keyword'}
        if hasattr(self, 'info'):
            fields = self.info['fields']
        for key, value in inputs.items():
            if key not in fields and value is not None:
                if 'translated_terms' == key:
                    result += join_with + join_with.join(value)
                else:
                    result += join_with + str(value)
        return result
