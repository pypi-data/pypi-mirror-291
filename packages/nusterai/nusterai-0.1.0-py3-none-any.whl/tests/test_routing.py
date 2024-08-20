import os
import unittest
from nusterai.routing import NusterAI

class TestNusterAI(unittest.TestCase):
    def setUp(self):
        # Setting up NusterAI with environment variables
        self.nuster_ai = NusterAI(
            gpt4omni_creds={
                "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            },
            gemini_flash_api_key=os.getenv("GOOGLE_API_KEY"),
            gemini_pro_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def test_easy_prompt_with_gpt4omni(self):
        response = self.nuster_ai.route_prompt("What is 2 + 2?")
        self.assertIsNotNone(response)
        print("GPT-4 Omni Response:", response)

    def test_intermediate_prompt_with_gemini_flash(self):
        response = self.nuster_ai.route_prompt("Explain photosynthesis.")
        self.assertIsNotNone(response)
        print("Gemini 1.5 Flash Response:", response)

    def test_advanced_prompt_with_gemini_pro(self):
        response = self.nuster_ai.route_prompt("Describe quantum entanglement.")
        self.assertIsNotNone(response)
        print("Gemini 1.5 Pro Response:", response)

if __name__ == "__main__":
    unittest.main()
