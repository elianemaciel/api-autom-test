import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

from app.repositories.llm.prompts.PromptBuilder import PromptBuilder
from assets.components import Method
from assets.repository.LLMRepository import LLMRepository

load_dotenv()


class ClaudeRepository(LLMRepository):

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = (
            os.getenv("CLAUDE_MODEL")
            or os.getenv("ANTHROPIC_MODEL")
            or "claude-sonnet-4-20250514"
        )

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
        result_content = self._create_message(
            request,
            system="You are an assistant that returns JSON output for the requested input"
        )

        print("<claude>" + str(result_content))

        result_json = result_content.replace("```json", "").replace("```", "").strip()
        return self._extract_methods_from_result(result_json, super().get_lang())

    def chat_completion(self, prompt):
        return self._create_message(
            prompt,
            system="You are an assistant that returns valid JSON only."
        )

    def _create_message(self, prompt, system):
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=0.2,
            system=system,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return "".join(
            block.text
            for block in message.content
            if getattr(block, "type", None) == "text"
        )

    def _extract_methods_from_result(self, result_json, language):
        print("_extract_methods_from_result")
        methods = []
        method_label = "method" if language == "en" else "metodo"
        returnType_label = "returnType" if language == "en" else "tipoRetorno"
        className_label = "className" if language == "en" else "nomeClasse"
        parameters_label = "parameters" if language == "en" else "parametros"
        name_label = "name" if language == "en" else "nome"
        type_label = "type" if language == "en" else "tipo"
        try:
            data = json.loads(result_json)
            for method in data:
                name = method[method_label].strip()
                return_type = method[returnType_label].lower().strip()
                class_name = method[className_label] if method[className_label].strip() else ""

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

        except Exception as error:
            print("Erro ao tentar gerar JSON a partir do resultado do Claude:", error)

        return methods

    def _enrich_llm_request(self, user_stories, language):
        builder = PromptBuilder()

        prompt = builder.enrich_llm_request(
            user_stories=user_stories,
            language=language
        )
        return prompt
