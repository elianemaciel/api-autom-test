import traceback

from assets import convertStories
from assets.repository.MethodCatcherRepository import MethodCatcherRepository


class NlpRepository(MethodCatcherRepository):

    def __init__(self):
        self.active = True
        self.user_story = ""
        self.max_retries = 1
        self.methods = []
        self.warnings = []
        self.curr_retry_number = 0
        self.exceptCount = 0

    def setup(self, user_story, language):
        self.active = True if language == 'pt' else False
        self.user_story = user_story
        self.max_retries = 1
        self.methods = []
        self.warnings = []
        self.curr_retry_number = 0
        self.exceptCount = 0

    def get_methods_from_user_stories(self):
        pass

    def get_current_state_percentage(self):
        return (self.curr_retry_number / self.max_retries) * 100

    def compute_extra_methods(self):
        if not self.active:
            print("Geração por NLP não está ativa")
            return
        # self.methods = self.get_methods_from_user_stories()
        #for i in range(0, self.max_retries):
        print("entrou em compute_extra_methods")
        if self.curr_retry_number < self.max_retries and self.exceptCount < 3:
            self.curr_retry_number += 1
            print("executando em compute_extra_methods")
            try:
                methods, warnings = convertStories.defineTestsFromStories(self.user_story)
                self.methods.extend(methods)
                self.warnings.extend(warnings)
            except:
                traceback.print_exc()
                self.exceptCount += 1
                self.max_retries += 1  # try again

    def get_caught_methods(self):
        return self.methods
