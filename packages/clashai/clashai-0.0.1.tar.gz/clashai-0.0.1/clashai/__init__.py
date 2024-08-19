__version__ = "0.0.1"

import requests

class Client:
    def __init__(self, api_key: str, model: str = None, system_prompt=None, base_url: str = None):
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.base_url =  base_url if base_url else "http://clashai.3utilities.com:25621"

    def make_request(self, content: str):
        sys_prompt = {"role": "system", "content": self.system_prompt if self.system_prompt else "You are a helpful assistant."}
        model = self.model if self.model else "chatgpt-4o-latest"
        api_key = self.api_key
        endpoint = "v1/chat/completions"
        url = f"{self.base_url}/{endpoint}"
        payload = {
                "model": model,
                "messages": [
                    sys_prompt
                ]
                                                                ,
            }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()