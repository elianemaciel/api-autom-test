import json

from app.repositories.LlmCatcherRepositoryFactory import LlmCatcherRepositoryFactory


class LlmTestCaseService:

    def __init__(self, methods, lang="pt", selected_ia="gpt", target_language="java"):
        self.methods = methods
        self.lang = lang
        self.selected_ia = selected_ia or "gpt"
        self.target_language = (target_language or "java").lower()

    def get(self):
        prompt = self._build_prompt()
        llm_client = LlmCatcherRepositoryFactory.create(
            user_story="",
            language=self.lang,
            llm_name=self.selected_ia
        )
        response = llm_client.chat_completion(prompt)
        return self._extract_json_response(response)

    def _build_prompt(self):
        language_instruction = self._language_instruction()
        payload = json.dumps(self.methods, ensure_ascii=False, indent=2)

        return f"""
{language_instruction}

Gere casos de teste unitários para os métodos informados usando as classes de equivalência recebidas.
Use apenas os dados enviados; não invente métodos, classes ou parâmetros que não estejam no JSON.
Para cada classe de equivalência, gere a quantidade de casos definida em numberOfCases.
Considere expectedOutputRange como o comportamento esperado.

Responda SOMENTE JSON válido, sem markdown, comentários ou texto extra.
Formato obrigatório para Java:
[
  {{
    "language": "java",
    "className": "<nome-da-classe-testada>",
    "packageName": "<pacote-ou-string-vazia>",
    "testClassName": "<nome-da-classe-de-teste>",
    "framework": "JUnit",
    "imports": ["<imports necessários>"],
    "tests": [
      {{
        "methodName": "<nome-do-metodo-de-teste>",
        "targetMethod": "<nome-do-metodo-testado>",
        "equivalenceClass": "<nome-da-classe-de-equivalencia>",
        "input": {{"<parametro>": "<valor>"}},
        "expected": "<valor-ou-condicao-esperada>",
        "code": "<codigo Java completo do metodo de teste>"
      }}
    ]
  }}
]

JSON de entrada:
{payload}
""".strip()

    def _language_instruction(self):
        if self.target_language == "java":
            return "A linguagem alvo é Java. Retorne os testes em formato JSON estruturado com código JUnit."

        return f"A linguagem alvo é {self.target_language}. Retorne os testes em JSON estruturado."

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

        return json.loads(json_text)
