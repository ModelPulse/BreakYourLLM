import json
import pandas as pd
import io
from openai import OpenAI

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_test_cases(question, guideline):
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
            Question: "{question}"
            guideline: "{guideline}"
            
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
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use gpt-4 if you have access to it
    messages=messages,
    temperature=0.3)

    # Parse the response as a Python list of dictionaries
    test_cases = eval(response.choices[0].message.content.strip())
    return test_cases


def generate_tests_from_csv(file):
    df = pd.read_csv(file)
    df = df.fillna("")
    
    # Do something with the dataframe
    # For example, returning the first few rows as a dictionary
    response = []
    
    for index, row in df.iterrows():
        question = row['question']
        answer = row['answer']
        guideline = row['guideline']
        test_cases = generate_test_cases(question, guideline)
        response.append({"question": question, "answer": answer, "test_cases": test_cases})
    
    print(response)
    return response
