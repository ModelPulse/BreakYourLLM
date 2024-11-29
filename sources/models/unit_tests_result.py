from typing import List
from sources.models.common_interface import BaseTest
from sources.helpers.testcase_evaluator import evaluate_answer_for_test

class AtomicTestCaseExecutionResult(BaseTest):

    def __init__(self, test_case, passed, reason):
        super().__init__()
        self.test_case: str = ""
        self.passed: bool = passed
        self.reason: str = reason


class ExecutionResult(BaseTest):

    def __init__(self, answer: str):
        super().__init__()
        self.answer: str = answer
        self.test_cases: List[AtomicTestCaseExecutionResult] = []

    def evaluate_responses(self, tests):
        for test in tests:
            # evaluate whether the answer follows the given test
            passed, reason = evaluate_answer_for_test(answer, test.test_case)
            self.test_cases.append(AtomicTestCaseExecutionResult(test, passed, reason))


class ParaphrasedQuestion(BaseTest):
    
    def __init__(self, question: str):
        super().__init__()
        self.question = question

        # List for result for each individual run for a paraphrased question
        self.execution_result: List[AtomicExecutionResult] = []

    def evaluate_responses(self, tests):
        for execution_result in self.execution_result:
            execution_result.evaluate_responses(tests)

# Different metrics for computation like accuracy, etc should go in here.