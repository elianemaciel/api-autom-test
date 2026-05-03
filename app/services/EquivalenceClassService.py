from app.repositories.llm.prompts.PromptBuilder import PromptBuilder
from app.repositories.LlmCatcherRepositoryFactory import LlmCatcherRepositoryFactory

class EquivalenceClassService:

    def __init__(self, methods, lang, selected_ia):
        self.methods = methods
        self.lang = lang
        self.selected_ia = selected_ia
        self.prompt_builder = PromptBuilder("equivalence")  # pt.json e en.json em arquivos separados

    def get(self):
        """
        Gera Classes de Equivalência com base nos métodos dados.
        """
        prompt = self.prompt_builder.build_equivalence_prompt(
            self.methods,
            self.lang
        )

        llm_client = LlmCatcherRepositoryFactory(self.selected_ia)
        response = llm_client.chat_completion(prompt)

        return response
