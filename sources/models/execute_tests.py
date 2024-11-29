# execute_test.py

import yaml
import requests
import json
import os
import logging
import re

class LLMExecutor:
    def __init__(self, config_file='config.yaml'):
        self.load_config(config_file)
        logging.basicConfig(level=logging.INFO)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)
        self.default_api = self.config.get('default_api')
        self.apis = self.config.get('apis', {})

    def call_llm_api(self, question, api_name=None, **kwargs):
        if api_name is None:
            api_name = self.default_api

        api_config = self.apis.get(api_name)
        if not api_config:
            raise ValueError(f"API '{api_name}' not found in configuration.")

        endpoint = api_config['endpoint']
        headers = api_config.get('headers', {}).copy()

        # Retrieve API key
        api_key = api_config.get('api_key')
        api_key_env_var = api_config.get('api_key_env_var')
        if api_key_env_var:
            api_key_env = os.getenv(api_key_env_var)
            if not api_key_env:
                raise EnvironmentError(f"Environment variable '{api_key_env_var}' is not set.")
            api_key = api_key_env
        if not api_key:
            raise ValueError(f"API key for '{api_name}' is not provided.")

        # Replace placeholders in headers
        for key, value in headers.items():
            if isinstance(value, str):
                headers[key] = value.format(api_key=api_key)

        # Prepare request body
        request_body_template = api_config.get('request_body')
        if not request_body_template:
            raise ValueError(f"Request body template for '{api_name}' is not provided.")

        # Merge any additional kwargs into the request body
        request_body = self.deep_format(request_body_template, question=question, **kwargs)

        # Convert request body to JSON string
        request_body_json = json.dumps(request_body)

        logging.info(f"Sending request to {api_name} API at {endpoint}")

        # Send the request
        response = requests.post(endpoint, headers=headers, data=request_body_json)

        # Handle response
        if response.status_code == 200:
            response_json = response.json()
            # Extract the answer based on the response path
            answer = self.extract_answer(response_json, api_config.get('response_path'))
            return answer
        else:
            logging.error(f"API request failed with status code {response.status_code}: {response.text}")
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    def deep_format(self, obj, **kwargs):
        """
        Recursively formats strings in a nested structure.
        """
        if isinstance(obj, dict):
            return {k: self.deep_format(v, **kwargs) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.deep_format(elem, **kwargs) for elem in obj]
        elif isinstance(obj, str):
            return obj.format(**kwargs)
        else:
            return obj

    def extract_answer(self, response_json, response_path):
        """
        Extracts the answer from the response JSON based on the response path.
        """
        if not response_path:
            return response_json  # Return the whole response if no path is provided

        try:
            # Split the path into keys
            keys = self.parse_response_path(response_path)
            result = response_json
            for key in keys:
                if isinstance(key, int):
                    result = result[key]
                else:
                    result = result[key]
            return result
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error extracting answer using path '{response_path}': {e}")
            raise

    def parse_response_path(self, path_str):
        """
        Parses the response path string into a list of keys/indexes.
        For example: 'choices[0].message.content' => ['choices', 0, 'message', 'content']
        """
        tokens = re.split(r'\.(?![^[]*\])', path_str)  # Split on dots not within brackets
        keys = []
        for token in tokens:
            match = re.match(r'(\w+)(\[(\d+)\])?', token)
            if match:
                key = match.group(1)
                index = match.group(3)
                keys.append(key)
                if index is not None:
                    keys.append(int(index))
            else:
                raise ValueError(f"Invalid token in response path: '{token}'")
        return keys
