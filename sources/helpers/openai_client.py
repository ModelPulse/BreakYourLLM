from openai import OpenAI
import os
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))