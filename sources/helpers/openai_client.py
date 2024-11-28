import os

# Uncomment the code below if you are using the OpenAI API directly
# from openai import OpenAI
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Comment the code below if you are not using the AzureOpenAI endpoint
from openai import AzureOpenAI
openai_client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version=os.getenv("API_VERSION"),
    api_key=os.getenv("API_KEY")
)