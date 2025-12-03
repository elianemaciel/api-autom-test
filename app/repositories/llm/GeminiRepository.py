import json


from assets.components import Method
from assets.repository.LLMRepository import LLMRepository
from google import genai
from dotenv import load_dotenv
import os
import app.repositories.llm.prompts.PromptBuilder as PromptBuilder

# Carrega o arquivo .env
load_dotenv()

class GeminiRepository(LLMRepository):

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))


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

        response = self.client.models.generate_content(model="gemini-2.5-flash", contents=request)
        result_content = response.text

        print("<gemini-1.5-flash>" + str(result_content))

        result_json = result_content.replace("```json", '').replace("```", '')

        return self._extract_methods_from_result(result_json, super().get_lang())

    def _extract_methods_from_result(self, result_json, language):
        print('_extract_methods_from_result')
        methods = []
        method_label = 'method' if language == 'en' else 'metodo'
        returnType_label = 'returnType' if language == 'en' else 'tipoRetorno'
        className_label = 'className' if language == 'en' else 'nomeClasse'
        parameters_label = 'parameters' if language == 'en' else 'parametros'
        name_label = 'name' if language == 'en' else 'nome'
        type_label = 'type' if language == 'en' else 'tipo'
        try:
            data = json.loads(result_json)
            for method in data:
                name = method[method_label].strip()
                return_type = method[returnType_label].lower().strip()
                class_name = method[className_label] if method[className_label].strip() else ''

                new_method = Method(
                    name=name,
                    class_name=class_name,
                    package_name="",
                    output_type=return_type,
                    params=[])

                for param in method[parameters_label]:
                    param_name = param[name_label].strip()
                    param_type = param[type_label].lower().strip()
                    new_method.add_param_by_arg(param_name, param_type)
                methods.append(new_method)

        except Exception as e:
            print("Erro ao tentar gerar JSON a partir do resultado do Gemini:", e)

        return methods

    def _enrich_llm_request(self, user_stories, language):
        builder = PromptBuilder("prompts")

        prompt = builder.enrich_llm_request(
            user_stories=user_stories,
            language=language
        )
        return prompt
