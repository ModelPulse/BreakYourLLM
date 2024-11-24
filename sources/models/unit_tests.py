from sources.models.common_interface import BaseTest
import pandas as pd
from collections.abc import Iterable
from typing import List
from sources.helpers.openai_client import openai_client
from sources.helpers.paraphrase_helper import paraphrase_question

class AtomicUnitTest(BaseTest):
    
    def __init__(self, test_case: str):
        
        self.test_case = test_case

    def test(self, question, llm_executor):
        # TODO: This design is subject to change. But the initial thought is to execute the question with LLM here and get the result.
        pass


class UnitTest(BaseTest):

    def __init__(self, question: str, guideline: str):
        super().__init__()
        self.question = question
        self.guideline = guideline
        self.test_cases: List[AtomicUnitTest] = []

    def generate_unit_tests(self):
        # ChatGPT-style prompt using messages for ChatCompletion
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a testing expert. Generate a list of test cases in Python dictionary format based on a question, and responses guideline provided by the user."
                ),
            },
            {
                "role": "user",
                "content": f"""
                Question: "{self.question}"
                guideline: "{self.guideline}"
                
                Breakdown the guideline into atomic test case assertions. They should be distinct and exhaustive test cases. Provide test cases as a Python list of dictionaries in this format. Do not add any extra field:
                [
                    {{
                        "test": "The test case assertion statement"
                    }},
                    ...
                ]
                Ensure each test case assertion is unique, independent of other test cases and evaluates whether the guideline is followed. Do not generate every possible test case, but have a assertion for each atomic rule in the guideline that must be true for a response that follows the guideline.
                """
            }
        ]

        # Call the OpenAI API with ChatCompletion
        response = openai_client.chat.completions.create(model="gpt-3.5-turbo", 
            messages=messages,
            temperature=0.3
        )

        # Parse the response as a Python list of dictionaries
        test_cases = eval(response.choices[0].message.content.strip())

        for test_case in test_cases:
            unit_test = AtomicUnitTest(test_case['test'])
            self.test_cases.append(unit_test)

        return test_cases

    def __iter__(self):
        return iter(self.test_cases)

    def paraphrase(self):
        n = os.env["PARAPHRASE_COUNT"]
        questions = paraphrase_question(self.question, n)
        self.paraphrased_questions = questions
        # TODO: Will make more sense if we utilize the UnitTestResult function to store or make storing of this more structured.


class UnitTests(BaseTest):
    def __init__(self, file=None):
        super().__init__()
        self.file = file
        self.unit_tests: List[UnitTest] = []

    def read_file(self):
        df = pd.read_csv(self.file)
        df = df.fillna("")
        
        response = []
        
        for index, row in df.iterrows():
            question = row['question']
            answer = row['answer']
            guideline = row['guideline']

            unit_test = UnitTest(question, guideline)
            self.unit_tests.append(unit_test)

    def generate_tests(self):
        if len(self.unit_tests)==0:
            self.read_file()
        
        for unit_test in self:
            unit_test.generate_unit_tests()
    
    def __iter__(self):
        return iter(self.unit_tests)
