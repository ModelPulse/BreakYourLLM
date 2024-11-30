from sources.metrics.base_metric import BaseMetric

class Accuracy(BaseMetric):

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


    def to_json(self):

        pass