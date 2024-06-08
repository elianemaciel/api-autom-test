from assets.llm.ChatGptTurboRepository import ChatGptTurboRepository
from assets.llm.PalmLlmRepository import PalmLlmRepository

from assets.repository.MethodCatcherRepository import MethodCatcherRepository
from assets.repository.NlpRepository import NlpRepository


class MultiMethodCatcherRepository(MethodCatcherRepository):
    # The basic ideia behind this Repository is to integrate both LLM repositories and NLP repository

    methodCatcherRepositories = []

    def setup(self, user_story, language, getAllMethodsAccepted=lambda: []):
        nlpRepository = NlpRepository()
        llmRepository1 = PalmLlmRepository()
        llmRepository2 = ChatGptTurboRepository()

        nlpRepository.setup(user_story, language, getAllMethodsAccepted)
        llmRepository1.setup(user_story, language, getAllMethodsAccepted)
        llmRepository2.setup(user_story, language, getAllMethodsAccepted)

        self.methodCatcherRepositories.append(llmRepository1)
        self.methodCatcherRepositories.append(llmRepository2)
        self.methodCatcherRepositories.append(nlpRepository)

    def get_methods_from_user_stories(self):
        #self.nlpRepository.get_methods_from_user_stories()
        #self.llmRepository.get_methods_from_user_stories()
        pass

    def get_current_state_percentage(self):

        #Tenho algumas possibilidades: somente um, nenhum, mais de um
        #A porcentagem tem que ser o menor != 0 deles - se existir- ou 0 em outro caso

        min_val = 100
        for repo in self.methodCatcherRepositories:
            curr = repo.get_current_state_percentage()
            if curr < min_val:
                min_val = curr
        return min_val

    def compute_extra_methods(self):
        for repo in self.methodCatcherRepositories:
            repo.compute_extra_methods()

    def get_caught_methods(self):
        methods = []
        for repo in self.methodCatcherRepositories:
            methods.extend(repo.get_caught_methods())
        return methods
