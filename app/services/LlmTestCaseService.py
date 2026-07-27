import ast
import json
import re

from app.repositories.llm.prompts.PromptBuilder import PromptBuilder
from app.repositories.LlmCatcherRepositoryFactory import LlmCatcherRepositoryFactory


class LlmResponseParseError(Exception):
    def __init__(self, message, raw_response):
        super().__init__(message)
        self.raw_response = raw_response


class LlmTestCaseService:

    def __init__(self, methods, lang="pt", selected_ia="gpt", target_language="java"):
        self.methods = methods
        self.lang = lang
        self.selected_ia = selected_ia or "gpt"
        self.target_language = (target_language or "java").lower()
        self.prompt_builder = PromptBuilder("tests-cases")  # pt.json e en.json em arquivos separados

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
        payload = json.dumps(self.methods, ensure_ascii=False, indent=2)
        prompt = self.prompt_builder.build_equivalence_prompt(
            self.methods,
            self.lang
        )
        print(prompt)
        return prompt

    def _language_instruction(self):
        if self.target_language == "java":
            return "A linguagem alvo é Java. Retorne os testes em formato JSON estruturado com código JUnit."

        return f"A linguagem alvo é {self.target_language}. Retorne os testes em JSON estruturado."

    def _extract_json_response(self, response):
        if not isinstance(response, str):
            return response

        json_text = self._extract_json_text(response)

        try:
            return json.loads(json_text)
        except json.JSONDecodeError as json_error:
            try:
                return self._parse_relaxed_json(json_text)
            except (ValueError, SyntaxError) as literal_error:
                raise LlmResponseParseError(
                    f"LLM returned invalid JSON: {json_error}. "
                    f"Fallback parser also failed: {literal_error}",
                    response
                ) from json_error

    def _parse_relaxed_json(self, json_text):
        try:
            return ast.literal_eval(json_text)
        except (ValueError, SyntaxError):
            normalized_text = re.sub(
                r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:',
                r'\1"\2":',
                json_text
            )
            normalized_text = re.sub(r'\btrue\b', 'True', normalized_text)
            normalized_text = re.sub(r'\bfalse\b', 'False', normalized_text)
            normalized_text = re.sub(r'\bnull\b', 'None', normalized_text)

            return ast.literal_eval(normalized_text)

    def _extract_json_text(self, response):
        text = re.sub(r"```(?:json)?", "", response, flags=re.IGNORECASE).strip()
        start = self._find_first_json_start(text)

        if start == -1:
            return text

        end = self._find_matching_json_end(text, start)
        if end == -1:
            raise LlmResponseParseError(
                "LLM returned incomplete JSON. The response was likely "
                "truncated before the closing bracket or brace.",
                response
            )

        return text[start:end + 1].strip()

    def _find_first_json_start(self, text):
        array_start = text.find("[")
        object_start = text.find("{")

        if array_start == -1:
            return object_start
        if object_start == -1:
            return array_start

        return min(array_start, object_start)

    def _find_matching_json_end(self, text, start):
        pairs = {
            "[": "]",
            "{": "}"
        }
        stack = [pairs[text[start]]]
        in_string = False
        quote_char = ""
        escaped = False

        for position in range(start + 1, len(text)):
            char = text[position]

            if escaped:
                escaped = False
                continue

            if in_string:
                if char == "\\":
                    escaped = True
                elif char == quote_char:
                    in_string = False
                continue

            if char in ('"', "'"):
                in_string = True
                quote_char = char
            elif char in pairs:
                stack.append(pairs[char])
            elif stack and char == stack[-1]:
                stack.pop()
                if not stack:
                    return position

        return -1
