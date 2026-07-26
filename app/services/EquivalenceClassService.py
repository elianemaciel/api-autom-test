import json

from app.repositories.llm.prompts.PromptBuilder import PromptBuilder
from app.repositories.LlmCatcherRepositoryFactory import LlmCatcherRepositoryFactory


class EquivalenceClassService:

    def __init__(self, methods, lang, selected_ia):
        self.methods = methods
        self.lang = lang
        self.selected_ia = selected_ia
        self.prompt_builder = PromptBuilder("equivalence")  # pt.json e en.json em arquivos separados

    def get(self):
        """
        Gera Classes de Equivalência com base nos métodos dados.
        """
        method = self._compact_method(self.methods[0])
        prompt = self.prompt_builder.build_equivalence_prompt(
            method,
            self.lang
        )
        print(prompt)
        llm_client = LlmCatcherRepositoryFactory.create(
            user_story="",
            language=self.lang,
            llm_name=self.selected_ia
        )
        response = llm_client.chat_completion(prompt)

        return self._extract_json_response(response)

    def _compact_method(self, method):
        return {
            "name": method.get("name"),
            "returnType": method.get("returnType"),
            "parameters": [
                {
                    "name": param.get("name"),
                    "type": param.get("type")
                }
                for param in method.get("parameters", [])
            ]
        }

    def _extract_json_response(self, response):
        if not isinstance(response, str):
            return response

        json_text = response.replace("```json", "").replace("```", "").strip()
        if not json_text.startswith(("[", "{")):
            array_start = json_text.find("[")
            object_start = json_text.find("{")

            if array_start != -1 and (object_start == -1 or array_start < object_start):
                json_text = json_text[array_start:json_text.rfind("]") + 1]
            elif object_start != -1:
                json_text = json_text[object_start:json_text.rfind("}") + 1]

        parsed_response = json.loads(json_text)
        if isinstance(parsed_response, dict) and "attribute" in parsed_response:
            return [parsed_response]

        return parsed_response
