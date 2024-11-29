from typing import List
from sources.models.common_interface import BaseTest

class AtomicTestCaseExecutionResult(BaseTest):

    def __init__(self):
        self.passed: bool = False
        self.reason: str = ""

class ExecutionResult(BaseTest):

    def __init__(self, answer: str):

        self.answer: str = answer
        self.test_cases: List[AtomicTestCaseExecutionResult] = []


class ParaphrasedQuestion(BaseTest):
    
    def __init__(self, question: str):
        
        self.question = question

        # List for result for each individual run for a paraphrased question
        self.execution_result: List[AtomicExecutionResult] = []


# Different metrics for computation like accuracy, etc should go in here.