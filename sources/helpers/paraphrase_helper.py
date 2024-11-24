import json
from sources.helpers.openai_client import openai_client

def paraphrase_question(original_question: str, n) -> dict:
    # Modified prompt to ask for a structured dictionary response
    prompt = f"""
    Please provide n = {n} paraphrased versions of the following question in a structured dictionary format:
    {{
        "paraphrased_questions": [
            "Paraphrased version 1",
            "Paraphrased version 2",
            "Paraphrased version 3",
            ...
            "Paraphrased version n"
        ]
    }}
    
    Original question: "{original_question}"
    """

    try:
        response = openai_client.chat.completions.create(
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