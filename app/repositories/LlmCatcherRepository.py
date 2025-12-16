class LlmCatcherRepository:

    def __init__(self, llm_repository):
        self.llm_repository = llm_repository

    def get_methods_from_user_stories(self):
        return self.llm_repository.get_methods_from_user_stories()

    def get_current_state_percentage(self):
        return self.llm_repository.get_current_state_percentage()

    def compute_extra_methods(self):
        self.llm_repository.compute_extra_methods()

    def get_caught_methods(self):
        return self.llm_repository.get_caught_methods()
