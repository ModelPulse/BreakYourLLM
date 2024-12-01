from sources.views.base_view import BaseView
from sources.models.unit_tests import UnitTests

class IncorrectResponses(BaseView):

    def __init__(self, results:UnitTests):
        self.results = results

    def json(self):
        for unit_test in self:
            for para_q in unit_test.paraphrased_questions:
                for execution_result in para_q.execution_result:
                    for test_case in execution_result.test_cases:
                        if test_case.passed:
                            pass