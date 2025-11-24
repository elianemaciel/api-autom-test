import threading
from abc import ABC

from assets.repository.MethodCatcherRepository import MethodCatcherRepository

# from assets.ui.windows.insert_methods_info_page import InsertMethodsInfoWidget

valid_accepted_data_types = {
    'string': 'String',
    'date': 'Date',
    'boolean': 'boolean',
    'bool': 'boolean',
    'integer': 'int',
    'int': 'int',
    'double': 'double',
    'char': 'char',
    'float': 'float'
}


class LLMRepository(MethodCatcherRepository, ABC):
    lock = threading.Lock()
    max_retries = 10
    number_of_acc_criteria = 5  # TODO: get this from user_story_txt
    min_amount_results = 2 * number_of_acc_criteria
    methods = []
    curr_amount_of_retries = 0
    user_story_txt = ""
    lang = ""
    isActive = True
    getAllMethodsAccepted = lambda: []

    def setup(self, user_story, language="pt", getAllMethodsAccepted=lambda: []):
        self.max_retries = 2
        given = 'dado' if language == "pt" else 'given'
        self.number_of_acc_criteria = user_story.lower().count(given) if isinstance(user_story, str) else len(user_story)
        self.min_amount_results = min(self.number_of_acc_criteria, 5)
        if self.min_amount_results == 0:
            self.min_amount_results = 2
        # self.min_amount_results = self.number_of_acc_criteria + max(self.number_of_acc_criteria, 5)
        self.curr_amount_of_retries = 0
        self.methods = []
        self.user_story_txt = user_story
        self.lang = language
        self.getAllMethodsAccepted = getAllMethodsAccepted

    def get_current_state_percentage(self):
        if not self.isActive:
            return 100
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
                sugg.output_type = "boolean"

            if sugg.output_type in valid_accepted_data_types:
                sugg.output_type = valid_accepted_data_types[sugg.output_type]
            else:
                continue

            if sugg.output_type == "void" or sugg.output_type == "Nenhum" or sugg.output_type == "None":
                # The method suggested must have an output type to use Equivalence Classes
                continue

            # Verify params validity
            valid_params = []
            for param in sugg.params:
                if param.type_name and param.type_name in valid_accepted_data_types:
                    param.type_name = valid_accepted_data_types[param.type_name]
                    valid_params.append(param)
            sugg.params = valid_params

            if len(sugg.params) == 0:
                # Do not add a method that doesn't have any parameter
                continue

            should_ignore = False
            for method in self.methods:
                if method.name.lower() == sugg.name.lower():
                    print(f"Method with name {sugg.name} already suggested before.")
                    should_ignore = True
                    break

            # if InsertMethodsInfoWidget.getMethods() and not should_ignore:
            #     for method in InsertMethodsInfoWidget.getMethods():
            if self.getAllMethodsAccepted() and not should_ignore:
                for method in self.getAllMethodsAccepted():
                    if method.name.lower() == sugg.name.lower():
                        print(f"Method with name {sugg.name} already suggested before.")
                        should_ignore = True
                        break

            if should_ignore:
                continue
            self.methods.append(sugg)

    def get_caught_methods(self):
        return self.methods

    def get_lang(self):
        return self.lang
