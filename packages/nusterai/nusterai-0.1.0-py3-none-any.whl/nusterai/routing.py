import textstat
from .llm_wrappers import GPT4Omni, GeminiProFlash, GeminiPro

class NusterAI:
    def __init__(self, gpt4omni_creds=None, gemini_flash_api_key=None, gemini_pro_api_key=None):
        self.gpt4omni_model = GPT4Omni(**(gpt4omni_creds or {}))
        self.gemini_flash_model = GeminiProFlash(api_key=gemini_flash_api_key)
        self.gemini_pro_model = GeminiPro(api_key=gemini_pro_api_key)

    def determine_difficulty(self, prompt):
        # Calculate Flesch-Kincaid Grade Level
        grade_level = textstat.flesch_kincaid_grade(prompt)
        return grade_level

    def route_prompt(self, prompt):
        difficulty = self.determine_difficulty(prompt)

        if difficulty <= 3:
            response = self.gemini_flash_model.generate(prompt)
        elif 4 <= difficulty <= 6:
            response = self.gemini_pro_model.generate(prompt)
        else:
            response = self.gpt4omni_model.generate(prompt)

        return response
