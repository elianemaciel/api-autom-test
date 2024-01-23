import re

import google.generativeai as palm

from assets.components import Method
from assets.repository.LLMRepository import LLMRepository
from environment import SecretConfig


def _extract_methods_from_result(result):
    class_name_pattern = re.compile(r"\*\*Class Name:\*\* (.+)")
    class_name_match = class_name_pattern.search(result)
    class_name = class_name_match.group(1) if class_name_match else ""

    pattern = r'\b(\w+)\s+(\w+)\(([^)]*)\)\s*'
    methods_pattern = re.compile(pattern)

    # Find methods
    methods_matches = methods_pattern.findall(result)

    # Print results
    methods = []
    print("Methods matches:" + str(len(methods_matches)))
    # print(methods_matches)

    for method_match in methods_matches:
        try:
            return_type, method_name, params = method_match
            if method_name == "isMinorAge" or method_name == "updateValues":
                continue
            param_list = params.split(", ")
            param_info = [param.split() for param in param_list if param]
            new_method = Method(name=method_name, class_name=class_name, package_name="", output_type=return_type,
                                params=[])

            for param_type, param_name in param_info:
                # TODO: verificações de que os dados e tudo o mais são válidos
                new_method.add_param_by_arg(param_name, param_type)

            methods.append(new_method)
        except:
            pass
    return methods


def _enrich_llm_request(user_stories):
    return "Use the below user story and acceptance criteria to suggest methods with the format of method signatures in Java and it's return, like examples below:\
    Boolean isMinorAge(Integer age)\
    Integer updateValues(String valueName, String keyForValue, Boolean isValueFinal)\
    \
    Besides That, I want a \"Class Name\" to those methods suggested, it can be any number of relevant methods returned." \
           " Do NOT give me methods with return value \"void\", because I will ignore them. Use the following user story as input: \
    \
    " + user_stories


class PalmLlmRepository(LLMRepository):

    def __init__(self):
        palm.configure(api_key=SecretConfig.API_KEY)  # todo: tirar API key antes de commitar

    def setup(self, user_story, language="pt"):
        self.isActive = language == "en"
        super().setup(user_story, language)

    def compute_extra_methods(self):
        if self.isActive and not (self.curr_amount_of_retries - self.max_retries > 0 and len(self.methods) < self.min_amount_results):
            new_suggestion = self.get_methods_from_user_stories()
            self.filter_and_add_valid_suggestions(new_suggestion)
            self.curr_amount_of_retries += 1

    def get_methods_from_user_stories(self):
        request = _enrich_llm_request(self.user_story_txt)
        result = palm.generate_text(prompt=request).result
        #print("Result é:")
        #print(result)
        methods = _extract_methods_from_result(result)
        #print("Os métodos criados:")
        #print("\n".join((lambda x: f"{x}")(method) for method in methods))
        return methods
