import json

from openai import OpenAI

from assets.components import Method
from assets.repository.LLMRepository import LLMRepository
from dotenv import load_dotenv
import os
from app.repositories.llm.prompts.PromptBuilder import PromptBuilder
from app.repositories.llm.MethodResponseParser import extract_methods_from_result

# Carrega o arquivo .env
load_dotenv()


class ChatGptTurboRepository(LLMRepository):

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

    def setup(self, user_story, language="pt", getAllMethodsAccepted=lambda: []):
        self.isActive = True
        super().setup(user_story, language, getAllMethodsAccepted)

    def compute_extra_methods(self):
        with super().lock:
            if self.isActive and not (self.curr_amount_of_retries - self.max_retries > 0 and len(self.methods) < self.min_amount_results):
                new_suggestion = self.get_methods_from_user_stories()
                self.filter_and_add_valid_suggestions(new_suggestion)
                self.curr_amount_of_retries += 1

    def get_methods_from_user_stories(self):
        request = self._enrich_llm_request(self.user_story_txt, super().get_lang())

        completion = self.client.chat.completions.create(
            model=os.getenv('OPEN_AI_MODEL'),
            messages=[
                {"role": "system",
                 "content": "You are an assistant that returns JSON output for the requested input"},
                {"role": "user", "content": request}
            ]
        )
        result_content = completion.choices[0].message.content
        result_json = result_content.replace("```json", '').replace('```', '')

        return self._extract_methods_from_result(result_json, super().get_lang())

    def _extract_methods_from_result(self, result_json, language):
        try:
            return extract_methods_from_result(result_json, language)
        except Exception:
            print('Erro ao tentar gerar Json a partir do resultado do gpt-3.5-turbo.')
            return []

    def _enrich_llm_request(self, user_stories, language):
        builder = PromptBuilder()

        prompt = builder.enrich_llm_request(
            user_stories=user_stories,
            language=language
        )
        return prompt
    
    def chat_completion(self, prompt):
        completion = self.client.chat.completions.create(
            model=os.getenv('OPEN_AI_MODEL'),
            messages=[
                {"role": "system",
                 "content": "You are an assistant that returns JSON output for the requested input"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_completion_tokens=4096
        )
        return completion.choices[0].message.content
