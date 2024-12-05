import json

from helpers.components import Method
from utils.llm.ChatGptTurboRepository import ChatGptTurboRepository


class PlnWithChatGptTurboRepository(ChatGptTurboRepository):

    def setup(self, incomplete_methods_json, language="pt", getAllMethodsAccepted=lambda: []):
        self.isActive = (language == "pt")
        super().setup(incomplete_methods_json, language, getAllMethodsAccepted)

    def _extract_methods_from_result(self, result_json, language):
        print('_extract_methods_from_result')
        methods = []
        method_label = 'metodo'
        returnType_label = 'tipoRetorno'
        className_label = 'nomeClasse'
        parameters_label = 'parametros'
        name_label = 'nome'
        type_label = 'tipo'
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

    def _enrich_llm_request(self, incomplete_methods, language):
        return 'Você é um assistente que retorna JSON como saída para o input que vou fornecer.\n' \
               'Complemente os métodos abaixo com os tipos de dados, que estão faltando. ' \
               'Os únicos tipos de dados permitidos são: int, String, float, double, char, boolean, Date.\n' \
               'Complemente mantendo o mesmo formato JSON:\n'\
                '' + self._get_json_str_from_method(incomplete_methods)

    def _get_json_str_from_method(self, methods):
        asStr = "[\n"
        for method in methods:
            asStr += f"""
            {{
                "metodo": "{method.method}",
                "parametros": [
            """
            for param in method.parameters if method.parameters else []:
                asStr += f"""
                        {{
                            "nome": "{param}",
                            "tipo": "?" 
                        }}                
                """

            asStr += f"""               
                ]
                "tipoRetorno": "?",
                "nomeClasse": "{method.className}"
            }},\n
            """
        asStr += "]"
        return asStr

