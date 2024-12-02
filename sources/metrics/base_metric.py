from sources.models.common_interface import BaseTest

class BaseMetric(BaseTest):

    def __init__(self, metric_name="", threshold=None):

        super().__init__()

        if metric_name=="":
            self.metric_name = type(self).__name__
        else:
            self.metric_name = metric_name
        

        self.metric_result = None
        self.threshold = None


    def passed(self):

        # Add your own logic to assess whether the metric value passed or failed
        raise Exception("Method not implemented")


    # def to_json(self):

    #     pass

"""
Dimensions guide to accessing numpy results array:

Dimension   Indexing entity
0           Questions in original CSV
1           Paraphrased questions corresponding to each question
2           Each individual repeitition of run for a paraphrased question
3           Result for the individual test case
"""