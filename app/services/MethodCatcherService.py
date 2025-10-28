import threading
import time
import traceback

# from assets.repository.MultiMethodCatcherRepository import MultiMethodCatcherRepository
from app.repositories.LlmCatcherRepositoryFactory import LlmCatcherRepositoryFactory
lock = threading.Lock()
while_lock = threading.Lock()

class MethodCatcherService:

    def __init__(self, user_story_txt="", language="en", llm_name="chatgpt"):
        self.user_story_txt = user_story_txt
        self.language = language
        self.method_catcher_repository = LlmCatcherRepositoryFactory.create(
            user_story=user_story_txt,
            language=language,
            llm_name=llm_name
        )
   
    def get(self):
        self._run_llm()
        return self.method_catcher_repository.get_caught_methods()

    def _run_llm(self):
        while True:
            with while_lock:
                self._update_methods_result_and_percentage()
                if self.method_catcher_repository.get_current_state_percentage() >= 100:
                    break
                time.sleep(1)
        print('Exited _run_llm')

    def _update_methods_result_and_percentage(self):
        with lock:
            # LLMRepository.get_extra_suggestions_from_user_story()
            self.method_catcher_repository.compute_extra_methods()
            curr_percentage = self.method_catcher_repository.get_current_state_percentage()
            # global progress_dialog
            if curr_percentage >= 100:
                # schedule.clear()
                return
