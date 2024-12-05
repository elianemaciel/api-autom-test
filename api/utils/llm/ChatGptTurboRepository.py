import json

from openai import OpenAI

from helpers.components import Method
from repository.LLMRepository import LLMRepository
import os

from dotenv import load_dotenv

load_dotenv()
class ChatGptTurboRepository(LLMRepository):

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv(OPEN_AI_API_KEY))

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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an assistant that returns JSON output for the requested input"},
                {"role": "user", "content": request}
            ]
        )
        print("<gpt-3.5-turbo>" + str(completion.choices[0].message.content))
        result_content = completion.choices[0].message.content
        result_json = result_content.replace("```json", '').replace('```', '')

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

        except:
            print('Erro ao tentar gerar Json a partir do resultado do gpt-3.5-turbo.')

        return methods

    def _enrich_llm_request(self, user_stories, language):
        if language == 'en':
            return 'You are an assistant that returns JSON output for the requested input.\n' \
                   'Use the user story with acceptance criteria below to suggest Java methods and class name.' \
                   'The valid data types are ONLY: int, String, float, double, char, boolean.\n' \
                   ' Use the following json format:\n' \
                   '[{\n' \
                   '    "method": "isMinorAge",\n' \
                   '   "parameters": [\n' \
                   '       {\n' \
                   '           "name": "classCode",\n' \
                   '           "type": "String"\n' \
                   '       }\n' \
                   '   ],\n' \
                   '    "returnType": "boolean",\n' \
                   '    "className": "AgeVerifier"\n' \
                   '},\n' \
                   '{\n' \
                   '...\n' \
                   '}]\n' \
                   'The user story is this:\n' \
                   '' + user_stories
        else:
            return 'Você é um assistente que retorna JSON como saída para o input que vou fornecer.\n' \
                   'Use a História de Usuário com Critérios de Aceitação abaixo pra sugerir métodos Java e ' \
                   'um nome de classe. ' \
                   'Os únicos tipos de dados permitidos são: int, String, float, double, char, boolean, Date.\n' \
                   'Use o seguinte formato JSON:\n' \
                   '[{\n' \
                   '    "metodo": "isMenorDeIdade",\n' \
                   '   "parametros": [\n' \
                   '       {\n' \
                   '           "nome": "codigoClasse",\n' \
                   '           "tipo": "String"\n' \
                   '       }\n' \
                   '   ],\n' \
                   '    "tipoRetorno": "boolean",\n' \
                   '    "nomeClasse": "VerificadorIdade"\n' \
                   '},\n' \
                   '{\n' \
                   '...\n' \
                   '}]\n' \
                   'A História de Usuário é a seguinte:\n' \
                   '' + user_stories
