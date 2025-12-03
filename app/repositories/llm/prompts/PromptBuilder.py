import json
import os

class PromptBuilder:

    def __init__(self, prompts_dir="methods"):
        self.prompts_dir = "prompts/" + prompts_dir

    def _load_prompt_file(self, language):
        lang_key = "en" if language == "en" else "pt"

        file_path = os.path.join(self.prompts_dir, f"{lang_key}.json")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file for language '{lang_key}' not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def enrich_llm_request(self, user_stories, language):
        prompt_data = self._load_prompt_file(language)

        if "template" not in prompt_data:
            raise KeyError(f"Missing 'template' key in prompt file for language '{language}'")

        template = prompt_data["template"]

        return template.format(user_stories=user_stories)
