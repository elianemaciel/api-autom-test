from abc import ABC

from assets.repository.MethodCatcherRepository import MethodCatcherRepository


# from decouple import config
# nlp = pt_core_news_md.load()


#
# def send_to_vercel_llm(text):
#     generated_text = ""
#     try:
#         vercel_ai.logger.setLevel(logging.ERROR)
#         client = vercel_ai.Client()
#         prompt = f"{text}. {random.randint(0, 1000)}"
#         params = {
#             "maximumLength": 1000
#         }
#         print("----------Response-----------")
#         # for chunk in client.generate("openai:gpt-3.5-turbo", prompt, params=params):
#         for chunk in client.generate("anthropic:claude-instant-v1", prompt, params=params):
#             # print(chunk, end="", flush=True)
#             generated_text += chunk
#         generated_text += "\n"
#
#     except Exception as e:
#         print(e.__str__())
#     print("-------------End-------------")
#     return generated_text
#
#
# def send_to_bard_llm(input_text):
#     # os.environ['_BARD_API_KEY'] = "dQjwaLPlSd0GNqXZwiLr8Q5rrsHWv7AIPAa0kNW-FjLwWWDbydBE950SgmIhvh0GmyC37w."
#     os.environ['_BARD_API_KEY'] = "dQjwaLPlSd0GNqXZwiLr8Q5rrsHWv7AIPAa0kNW-FjLwWWDbydBE950SgmIhvh0GmyC37w."
#     bard_output = Bard().get_answer(input_text)['content']
#     print("Bard output:")
#     print(bard_output)
#     return bard_output

#
# def generate_methods_suggestion(user_story_txt):
#     # llm_method_suggestion_result = send_to_bard_llm(enrich_llm_request(user_story_txt))
#     # llm_method_suggestion_result = send_to_palm_llm(enrich_llm_request(user_story_txt))
#     llm_method_suggestion_result = palm_llm.get_methods_from_user_stories(user_story_txt)
#     # llm_method_suggestion_result = send_to_llm(enrich_llm_request(user_story_txt))
#
#     return llm_method_suggestion_result
#

class LLMRepository(MethodCatcherRepository, ABC):
    max_retries = 10
    number_of_acc_criteria = 5  # TODO: get this from user_story_txt
    min_amount_results = 2 * number_of_acc_criteria
    methods = []
    curr_amount_of_retries = 0
    user_story_txt = ""
    lang = ""
    isActive = True

    def setup(self, user_story, language="pt"):
        print("LLMRepository setup")
        self.max_retries = 10
        self.number_of_acc_criteria = 5  # TODO: get this from user_story_txt
        self.min_amount_results = 2 * self.number_of_acc_criteria
        self.curr_amount_of_retries = 0
        self.methods = []
        self.user_story_txt = user_story
        self.lang = language

    def get_current_state_percentage(self):
        percentage_result = (len(self.methods) / self.min_amount_results) * 100
        percentage_retry = (self.curr_amount_of_retries / self.max_retries) * 100
        return max(percentage_result, percentage_retry)

    def get_methods_from_user_stories(self):
        raise NotImplementedError("Subclasses must implement this method. Should return a list of Method")

    def filter_and_add_valid_suggestions(self, new_sugg):
        for sugg in new_sugg:
            if sugg.output_type == "" and sugg.name == "":
                # This is only the definition of class name. Do not create a Method for that info alone
                continue

            if sugg.output_type == "void":
                sugg.output_type = "Boolean"

            if sugg.output_type == "" or sugg.output_type == "void" or sugg.output_type == "Nenhum":
                # The method suggested doesn't have a return suggestion, so don't consider it as a possibility
                continue

            should_ignore = False
            for method in self.methods:
                if method.name == sugg.name:
                    print(f"Method with name {sugg.name} already exists.")
                    should_ignore = True
                    break
            if should_ignore:
                continue
            self.methods.append(sugg)

    def get_caught_methods(self):
        return self.methods
