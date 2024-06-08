
# generic method catcher repository interface. Must be implemented by each LLM repository and by the regular
# classic method to retrieve methods, the one that doesn't use LLM.

class MethodCatcherRepository:
    def setup(self, user_story, language, getAllMethodsAccepted):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_methods_from_user_stories(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_current_state_percentage(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def compute_extra_methods(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_caught_methods(self):
        raise NotImplementedError("Subclasses must implement this method.")

