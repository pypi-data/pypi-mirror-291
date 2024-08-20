import os
import google.generativeai as genai
from openai import AzureOpenAI
import logging

class GPT4Omni:
    def __init__(self, api_key=None, azure_endpoint=None, deployment_name=None):
        self.client = AzureOpenAI(
            api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = deployment_name or "gpt-4o"  # Use the provided model name

    def generate(self, prompt):
        logging.info("Generating content with OpenAI API")
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
                max_tokens=1024,
                seed=43,
            )
            logging.info("Content generated successfully")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating content: {e}")
            raise


class GeminiProFlash:
    def __init__(self, api_key=None):
        genai.configure(api_key=api_key or os.getenv('API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate(self, prompt):
        config = self._create_config()
        response = self.model.generate_content(prompt, generation_config=config)
        return response.text

    def _create_config(self):
        return genai.GenerationConfig(
            max_output_tokens=1024,
            temperature=0,
            top_p=0.9,
        )


class GeminiPro:
    def __init__(self, api_key=None):
        genai.configure(api_key=api_key or os.getenv('API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def generate(self, prompt):
        config = self._create_config()
        response = self.model.generate_content(prompt, generation_config=config)
        return response.text

    def _create_config(self):
        return genai.GenerationConfig(
            max_output_tokens=1024,
            temperature=0,
            top_p=0.9,
        )
