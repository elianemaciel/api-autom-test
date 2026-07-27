import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

from app.repositories.llm.prompts.PromptBuilder import PromptBuilder
from app.repositories.llm.MethodResponseParser import extract_methods_from_result
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
            system="You are an assistant that returns JSON output for the requested input",
            max_tokens=self._env_positive_int("CLAUDE_METHOD_MAX_TOKENS", 8192),
            continue_on_truncation=True
        )

        print("<claude>" + str(result_content))

        result_json = result_content.replace("```json", "").replace("```", "").strip()
        return self._extract_methods_from_result(result_json, super().get_lang())

    def chat_completion(self, prompt):
        return self._create_message(
            prompt,
            system="You are an assistant that returns valid JSON only.",
            max_tokens=self._env_positive_int("CLAUDE_TEST_MAX_TOKENS", 8192),
            continue_on_truncation=True
        )

    def _create_message(
        self,
        prompt,
        system,
        max_tokens=4096,
        continue_on_truncation=False
    ):
        messages = [{"role": "user", "content": prompt}]
        full_response = ""
        max_continuations = self._env_positive_int("CLAUDE_MAX_CONTINUATIONS", 3)

        for continuation_index in range(max_continuations + 1):
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.2,
                system=system,
                messages=messages,
            )
            response_part = self._message_text(message)
            full_response = self._append_without_overlap(full_response, response_part)

            if message.stop_reason != "max_tokens":
                return full_response

            if not continue_on_truncation or continuation_index >= max_continuations:
                return full_response

            print(
                "Claude response reached max_tokens. "
                f"Requesting continuation {continuation_index + 1}/{max_continuations}."
            )
            messages = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": full_response},
                {
                    "role": "user",
                    "content": (
                        "Your JSON response was truncated by the output token limit. "
                        "Continue exactly from the next character after your previous "
                        "response. Return only the missing JSON continuation, without "
                        "repeating previous content, markdown, or explanations."
                    )
                }
            ]

        return full_response

    def _message_text(self, message):
        return "".join(
            block.text
            for block in message.content
            if getattr(block, "type", None) == "text"
        )

    def _append_without_overlap(self, current_response, response_part):
        if not current_response:
            return response_part

        if response_part.startswith(current_response):
            return response_part

        max_overlap = min(len(current_response), len(response_part), 4096)
        for overlap_size in range(max_overlap, 0, -1):
            if current_response[-overlap_size:] == response_part[:overlap_size]:
                return current_response + response_part[overlap_size:]

        return current_response + response_part

    def _env_positive_int(self, name, default):
        try:
            return max(1, int(os.getenv(name, default)))
        except (TypeError, ValueError):
            return default

    def _extract_methods_from_result(self, result_json, language):
        print("_extract_methods_from_result")
        try:
            return extract_methods_from_result(result_json, language)
        except Exception as error:
            print("Erro ao tentar gerar JSON a partir do resultado do Claude:", error)
            return self._repair_and_extract_methods(result_json, language)

    def _repair_and_extract_methods(self, result_json, language):
        repair_prompt = (
            "Correct the invalid JSON below without changing, removing, or adding "
            "methods, parameters, or equivalence classes. Fix only JSON syntax. "
            "Return the complete corrected JSON only, without markdown or explanations.\n\n"
            f"{result_json}"
        )

        try:
            repaired_json = self._create_message(
                repair_prompt,
                system="You repair invalid JSON and return valid JSON only.",
                max_tokens=self._env_positive_int("CLAUDE_METHOD_MAX_TOKENS", 8192),
                continue_on_truncation=True
            )
            return extract_methods_from_result(repaired_json, language)
        except Exception as error:
            print("Erro ao reparar JSON retornado pelo Claude:", error)
            return []

    def _enrich_llm_request(self, user_stories, language):
        builder = PromptBuilder()

        prompt = builder.enrich_llm_request(
            user_stories=user_stories,
            language=language
        )
        return prompt
