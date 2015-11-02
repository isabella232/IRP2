__author__ = 'jansen'
from collection import Collection

class Dummy(Collection):

    def setClassName(self, classname):
        self.classname = classname

    def keywordResultsCount(self, inputs):
        self.inputs = inputs
        url = "http://www.example.com/search.html"
        self.results_url = url
        self.results_count = 0
        return self

    def emit(self):
        result = {
            'class': self.classname,
            'results_count': self.results_count,
            'results_url': self.results_url,
            'inputs': self.inputs
        }
        return result
