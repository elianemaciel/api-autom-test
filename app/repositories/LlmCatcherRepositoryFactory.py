from app.repositories.LlmCatcherRepository import LlmCatcherRepository
from app.repositories.llm.ChatGptTurboRepository import ChatGptTurboRepository
from app.repositories.llm.PalmLlmRepository import PalmLlmRepository
from assets.repository.NlpWithChatGptTurboRepository import NlpWithChatGptTurboRepository

class LlmCatcherRepositoryFactory:
    
    LLM_MAP = {
        "chatgpt": ChatGptTurboRepository,
        "palm": PalmLlmRepository,
        "nlp": NlpWithChatGptTurboRepository  # exemplo de outro LLM
    }
    @staticmethod
    def create(user_story, language, llm_name, getAllMethodsAccepted=lambda: []):
        
        llm_repository = LlmCatcherRepositoryFactory._instantiate_llm(llm_name)

        # Configura o LLM
        llm_repository.setup(user_story, language, getAllMethodsAccepted)

        # Retorna o repository encapsulando o LLM
        return LlmCatcherRepository(llm_repository=llm_repository)

    @staticmethod
    def _instantiate_llm(llm_name):
        llm_class = LlmCatcherRepositoryFactory.LLM_MAP.get(llm_name.lower())
        if not llm_class:
            raise ValueError(f"LLM desconhecido: {llm_name}")
        return llm_class()