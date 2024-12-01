from typing import List
from sources.models.common_interface import BaseTest
from sources.helpers.testcase_evaluator import evaluate_answer_for_test
import os
import numpy as np

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
            passed, reason = evaluate_answer_for_test(self.answer, test.test_case)
            self.test_cases.append(AtomicTestCaseExecutionResult(test, passed, reason))

    def get_evaluation_result_as_numpy(self):
        results = []
        for test in self.test_cases:
            results.append(test.passed)
        return np.array(results)


class ParaphrasedQuestion(BaseTest):
    
    def __init__(self, question: str):
        super().__init__()
        self.question = question

        # List for result for each individual run for a paraphrased question
        self.execution_result: List[ExecutionResult] = []

    def execute(self, llm_executor):
        n = int(os.getenv("QUESTION_REPETITION_COUNT"))
        for _ in range(n):
            answer = llm_executor.call_llm_api(self.question)
            self.execution_result.append(ExecutionResult(answer))

    def evaluate_responses(self, tests):
        for execution_result in self.execution_result:
            execution_result.evaluate_responses(tests)

    def get_evaluation_result_as_numpy(self):
        results = []
        for execution_result in self.execution_result:
            results.append(execution_result.get_evaluation_result_as_numpy())
        return np.array(results)

# TODO: Different metrics for computation like accuracy, etc should go in here.