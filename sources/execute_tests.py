import json
import pandas as pd
import io
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Optional
from routers.answer import  QuestionRequest, AnswerResponse, answer_question


import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to paraphrase question using OpenAI
async def paraphrase_question(original_question: str) -> dict:
    # Modified prompt to ask for a structured dictionary response
    prompt = f"""
    Please provide 1 paraphrased versions of the following question in a structured dictionary format:
    {{
        "paraphrased_questions": [
            "Paraphrased version 1",
            "Paraphrased version 2",
            "Paraphrased version 3",
        ]
    }}
    
    Original question: "{original_question}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use another model if preferred
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        # Parse the response to get a dictionary
        result_text = response.choices[0].message.content.strip()

        try:
            result_dict = json.loads(result_text)
            paraphrased_questions = result_dict.get("paraphrased_questions", [])
            return paraphrased_questions
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Failed to parse OpenAI response {result_text} into dictionary format.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating paraphrases: {e}")


# Function to evaluate test case using OpenAI
async def evaluate_test_case(answer: str, test: str) -> TestCaseResult:
    # Modify the prompt to request a structured response in dictionary format
    prompt = f"""
    Answer: '{answer}'
    Test: {test}
    
    Please evaluate whether the answer satisfies the test.
    Return a JSON-like dictionary with the following structure:
    {{
        "passed": <true/false>,
        "reason": <explanation if failed, empty string if passed>
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use another model if preferred
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        # Parse the response from OpenAI as a dictionary
        result_text = response.choices[0].message.content.strip()

        # Try to parse the result as JSON (a dictionary)
        try:
            result_dict = json.loads(result_text)
            passed = result_dict.get("passed", False)
            reason = result_dict.get("reason", "")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Failed to parse OpenAI response {result_text} into dictionary format.")

        return TestCaseResult(test=test, passed=passed, reason=reason)

    except Exception as e:
        # Handle OpenAI API errors
        raise HTTPException(status_code=500, detail=f"Error evaluating test case: {e}")

# Endpoint to execute tests for each question
@execution_router.post("/execute_tests", response_model=List[QuestionTestResult])
async def execute_endpoint(question_items: List[QuestionItem]):
    results = []

    for item in question_items:
        paraphrased_versions = await paraphrase_question(item.question)

        print(paraphrased_versions)

        # For each paraphrased version, ask OpenAI 3 times and evaluate test cases
        all_paraphrased_results = []

        for paraphrased_question in paraphrased_versions:
            paraphrased_answers = []
            paraphrased_test_results = []

            for _ in range(5):  # Ask each paraphrased question 3 times
                # Call /answer to get an answer for the paraphrased question
                answer_response = await answer_question(QuestionRequest(question=paraphrased_question))
                answer = answer_response.answer

                # Evaluate each test case with the answer using OpenAI
                test_results = []
                for test_case in item.test_cases:
                    test_result = await evaluate_test_case(answer, test_case.test)
                    test_results.append(test_result)
                    print(test_result)

                paraphrased_answers.append(answer)
                paraphrased_test_results.append(test_results)

            # Collect the results for this paraphrased question
            all_paraphrased_results.append(ParaphrasedQuestionResults(
                paraphrased_question=paraphrased_question,
                answers=paraphrased_answers,
                test_results=paraphrased_test_results
            ))

        # Collect results for the original question
        results.append({
            "question": item.question,
            "paraphrased_results": all_paraphrased_results
        })

    return results