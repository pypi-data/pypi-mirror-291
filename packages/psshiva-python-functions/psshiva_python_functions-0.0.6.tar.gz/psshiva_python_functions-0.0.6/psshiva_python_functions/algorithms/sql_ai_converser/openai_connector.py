from openai import AzureOpenAI
from typing import List, Dict

class OpenAIConnector:
    
    def __init__(self, api_key: str = None, azure_endpoint: str = None, api_version: str = None, azure_ad_token_provider: str = None) -> None:
        # Check for empty strings and raise errors
        if not api_key and not azure_ad_token_provider:
            raise ValueError("Either api_key or azure_ad_token_provider must be provided.")
        if api_key == "":
            raise ValueError("api_key cannot be an empty string.")
        if azure_ad_token_provider == "":
            raise ValueError("azure_ad_token_provider cannot be an empty string.")
        if azure_endpoint == "":
            raise ValueError("azure_endpoint cannot be an empty string.")
        if api_version == "":
            raise ValueError("api_version cannot be an empty string.")
        
        self.api_key = api_key
        self.azure_endpoint = azure_endpoint
        self.api_version = api_version
        self.azure_ad_token_provider = azure_ad_token_provider
        
        # Initialize the AzureOpenAI client with provided parameters
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        # Initialize the AzureOpenAI client with provided parameters
        if self.api_key:
            return AzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.azure_endpoint,
                api_version=self.api_version
            )
        elif self.azure_ad_token_provider:
            # Initialize using azure_ad_token_provider
            return AzureOpenAI(
                token_provider=self.azure_ad_token_provider,
                azure_endpoint=self.azure_endpoint,
                api_version=self.api_version
            )
    
    # Example method to use the client
    def get_response(self, messages: List[Dict[str, str]], model: str, *args, **kwargs) -> str:
        # Validate that messages is a list of dictionaries with 'role' and 'content' keys
        if not all(isinstance(msg, dict) and 'role' in msg and 'content' in msg for msg in messages):
            raise ValueError("Each message must be a dictionary with 'role' and 'content' keys.")
        
        # Create a dictionary for the request parameters
        request_params = {
            'model': model,
            'messages': messages,
            **kwargs  # Include additional parameters from kwargs
        }
        
        # Call the chat completions API
        response = self.client.chat.completions.create(
            **request_params
        )
        
        # Check if the response contains choices and return the content of the first message
        if response.choices:
            return response.choices[0].message['content']
        else:
            raise ValueError("No choices found in the response.")
