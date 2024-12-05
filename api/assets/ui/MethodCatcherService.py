import threading
import time
import traceback

from repository.MultiMethodCatcherRepository import MultiMethodCatcherRepository

lock = threading.Lock()
while_lock = threading.Lock()
method_catcher_repository = MultiMethodCatcherRepository()


def get(user_story_txt, language):
    method_catcher_repository.setup(user_story_txt, language)
    _run_llm()
    return method_catcher_repository.get_caught_methods()


def _run_llm():
    while True:
        with while_lock:
            _update_methods_result_and_percentage()
            if method_catcher_repository.get_current_state_percentage() >= 100:
                break
            time.sleep(1)
    print('Exited _run_llm')


def _update_methods_result_and_percentage():
    with lock:
        # LLMRepository.get_extra_suggestions_from_user_story()
        method_catcher_repository.compute_extra_methods()
        curr_percentage = method_catcher_repository.get_current_state_percentage()
        # global progress_dialog
        if curr_percentage >= 100:
            # schedule.clear()
            return
