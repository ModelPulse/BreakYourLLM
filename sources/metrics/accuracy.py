from sources.metrics.base_metric import BaseMetric

class Accuracy(BaseMetric):

    def __init__(self, metric_name="", threshold=None):

        super().__init__()

        if metric_name=="":
            self.metric_name = type(self).__name__
        else:
            self.metric_name = metric_name
        

        self.metric_result = None
        self.metric_result_question_wise = []
        self.metric_result_question_test_wise = []
        self.threshold = None


    def passed(self):

        # Add your own logic to assess whether the metric value passed or failed
        raise Exception("Method not implemented")


    def get_metric_value(self, result_array):

        self.metric_result = result_array.mean()
        self.metric_result_question_wise = result_array.mean(axis=(1, 2, 3)).tolist()
        self.metric_result_question_test_wise = result_array.mean(axis=(1, 2)).tolist()
        return self.metric_result