import traceback

from assets import convertStories
from app.repositories.llm.PlnWithChatGptTurboRepository import PlnWithChatGptTurboRepository

from assets.repository.NlpRepository import NlpRepository


class NlpWithChatGptTurboRepository(NlpRepository):

    def __init__(self):
        super().__init__()
        self.plnLlmRepository = PlnWithChatGptTurboRepository()

    def compute_extra_methods(self):
        if not self.active:
            print("Geração por NLP não está ativa")
            return
        if self.curr_retry_number < self.max_retries and self.exceptCount < 3:
            self.curr_retry_number += 1
            try:
                methods, warnings = convertStories.defineTestsFromStories(self.user_story)
                # chama LLM para complementar os dados faltantes dos métodos
                self.plnLlmRepository.setup(incomplete_methods_json=methods)
                self.plnLlmRepository.compute_extra_methods()
                methods = self.plnLlmRepository.get_caught_methods()
                self.methods.extend(methods)
                self.warnings.extend(warnings)
            except:
                traceback.print_exc()
                self.exceptCount += 1
                self.max_retries += 1  # try again
