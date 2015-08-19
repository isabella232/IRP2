class Collection(object):
    results_count = None
    results_url = None
    inputs = None

    def emit(self):
        result = {
            'class': type(self).__name__,
            'results_count': self.results_count,
            'results_url': self.results_url,
            'inputs': self.inputs
        }
        return result

    def keywordResultsCount(self, inputs):
        # Performs a keyword query on the collections and counts the results.
        # Results are stored in instance variables.
        # Returns self.
        pass
