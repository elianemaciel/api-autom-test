from assets.llm.PalmLlmRepository import PalmLlmRepository

from assets.repository.MethodCatcherRepository import MethodCatcherRepository
from assets.repository.NlpRepository import NlpRepository


class MultiMethodCatcherRepository(MethodCatcherRepository):
    # The basic ideia behind this Repository is to integrate both LLM methdod repositories and NLP repository

    nlpRepository = NlpRepository()
    llmRepository = PalmLlmRepository()
    lastPercentage = 0

    def setup(self, user_story, language):
        self.nlpRepository.setup(user_story, language)
        self.llmRepository.setup(user_story, language)

    def get_methods_from_user_stories(self):
        #self.nlpRepository.get_methods_from_user_stories()
        #self.llmRepository.get_methods_from_user_stories()
        pass

    def get_current_state_percentage(self):
        nlpPercentage = self.nlpRepository.get_current_state_percentage()
        llmPercentage = self.llmRepository.get_current_state_percentage()
        # Tenho 3 possibilidades: somente um, somente o outro ou os 2.
        # Se um dos 2 for zero, considera a porcentagem como sendo do outro
        # Se nenhum dos 2 for zero, a porcentagem deve ser min dos dois
        # A menos que a porcentagem anterior era maior. nesse caso, repete a porcentagem anterior.
        if nlpPercentage == 0 or llmPercentage == 0:
            self.lastPercentage = llmPercentage if llmPercentage != 0 else nlpPercentage
            return self.lastPercentage
        minPercentage = min(nlpPercentage, llmPercentage)
        result = max(self.lastPercentage, minPercentage)
        self.lastPercentage = result
        return self.lastPercentage

    def compute_extra_methods(self):
        self.nlpRepository.compute_extra_methods()
        self.llmRepository.compute_extra_methods()

    def get_caught_methods(self):
        methods = []
        methods.extend(self.llmRepository.get_caught_methods())
        methods.extend(self.nlpRepository.get_caught_methods())
        return methods
