import json
from sources.helpers.openai_client import openai_client
import os

def evaluate_answer_for_test(answer: str, test):
    # Modified prompt to ask for a structured dictionary response
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
        response = openai_client.chat.completions.create(
            model=os.getenv("MODEL"),  # You can use another model if preferred
            messages=[{"role": "user", "content": prompt}],
            response_format ={ "type": "json_object" },
            temperature=0.7
        )

        # Parse the response to get a dictionary
        result_text = response.choices[0].message.content.strip()

        try:
            result_dict = json.loads(result_text)
            passed = result_dict.get("passed", False)
            passed = bool(passed)
            reason = result_dict.get("reason", "")
            return passed, reason
        except json.JSONDecodeError:
            raise Exception(f"Failed to parse OpenAI response {result_text} into dictionary format.")

    except Exception as e:
        raise Exception(f"Error generating paraphrases: {e}")