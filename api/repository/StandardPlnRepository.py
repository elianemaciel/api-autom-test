import logging
import random
import re

import vercel_ai

from assets import convertStories
from assets.components import Method


def send_to_llm(text):
    generated_text = ""
    try:
        vercel_ai.logger.setLevel(logging.WARN)
        client = vercel_ai.Client()
        prompt = f"{text}. {random.randint(0, 1000)}"
        params = {
            "maximumLength": 1000
        }
        print("----------Response-----------")
        for chunk in client.generate("openai:gpt-3.5-turbo", prompt, params=params):
            print(chunk, end="", flush=True)
            generated_text += chunk
        print()
    except Exception as e:
        print(e.__traceback__)
    return generated_text
    print("-------------End-------------")

def generate_methods_suggestion(user_story_txt):
    llm_method_suggestion_result = send_to_llm(user_story_txt)
    method_descriptions = re.split(r"Método \d+:", llm_method_suggestion_result)

    # Remove any leading/trailing whitespace from each element
    method_descriptions = [method.strip() for method in method_descriptions if method.strip()]

    methods = []
    class_name = ""
    for method_descr in method_descriptions:

        match = re.search(r'Classe:\s*([^\n]*)', method_descr)
        class_name = match.group(1) if match else class_name

        match = re.search(r'Tipo de Retorno:\s*([^\n]*)', method_descr)
        return_type = match.group(1) if match else ""

        match = re.search(r'Nome do Método:\s*([^\n]*)', method_descr)
        method_name = match.group(1) if match else ""

        if return_type == "" and method_name == "":
            # This is only the definition of class name. Do not create a Method for that info alone
            continue

        new_method = Method(name=method_name, class_name=class_name, package_name="", output_type=return_type,
                            params=[])

        param_matches = re.findall(r'- (.*?) \((.*?)\)', method_descr)
        for param_name, param_type in param_matches:
            if type(param_name) != str or param_name.startswith('['):
                print('(1)Ignoring invalid param "' + str(param_name) + '"')
                continue
            new_method.add_param_by_arg(param_name, param_type)

        methods.append(new_method)
    return methods


def send_user_story(user_story_txt, amount_of_repetitions, exec_after_each_repetition):
    methods = []
    for i in range(0, amount_of_repetitions):
        methods.extend(generate_methods_suggestion(user_story_txt))
        exec_after_each_repetition(i)

    return methods, []
    return convertStories.defineTestsFromStories(user_story_txt)

    # caso tenha ocorrido warnings, mostra a lista numa tela de warning, com opção de continuar ou de mudar o user story
    # caso tenha ocorrido warnings e o usuário optado por continuar, encaminha para tela de seleção de métodos
    # caso não tenha ocorrido erro, encaminha para tela de seleção dos métodos

    # Levanta error no popup e não muda de tela caso tenha ocorrido erro.
