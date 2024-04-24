import threading
import time
import traceback

import schedule
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QProgressDialog

from assets.repository.MultiMethodCatcherRepository import MultiMethodCatcherRepository

lock = threading.Lock()
while_lock = threading.Lock()
progress_dialog = None
llm_execution_thread = None

# method_catcher_repository = LLMRepository
# method_catcher_repository = PalmLlmRepository()
# method_catcher_repository = NlpRepository()
method_catcher_repository = MultiMethodCatcherRepository()


def run(user_story_txt, language, parent=None):
    global llm_execution_thread, progress_dialog

    method_catcher_repository.setup(user_story_txt, language)

    scheduler_thread = schedule.Scheduler()
    llm_execution_thread = threading.Thread(target=_run_llm, args=(scheduler_thread,))
    # llm_execution_thread = threading.Thread(target=_run_llm)
    llm_execution_thread.setDaemon(True)
    llm_execution_thread.start()
    scheduler_thread.clear()

    progress_dialog = QProgressDialog("Generating method suggestions...", "Abort Generation", 0, 100)
    parent.addWidget(progress_dialog)
    progress_dialog.resize(400, 200)
    progress_dialog.setWindowTitle("Method suggestions")
    icon = QIcon("../img/logo.jpg")  # Replace with the path to your icon file
    progress_dialog.setWindowIcon(icon)
    progress_dialog.exec_()

    llm_execution_thread.join()

    return method_catcher_repository.get_caught_methods()


def _run_llm(scheduler_thread):
    schedule.every().seconds.do(_update_methods_result_and_percentage)
    # while LLMRepository.get_current_state_percentage() < 100:
    while True:
        print('entrou no while')
        with while_lock:
            print('entrou no while_lock')
            if method_catcher_repository.get_current_state_percentage() >= 100:
                break
            try:
                print("running pending")
                schedule.run_pending()
            except Exception as e:
                traceback.print_exc()
                print("Error while getting extra methods suggestions from user story: " + e.__str__())
            time.sleep(1)
    schedule.clear()


def _update_methods_result_and_percentage():
    with lock:
        print("_update_methods_result_and_percentage start")
        # LLMRepository.get_extra_suggestions_from_user_story()
        method_catcher_repository.compute_extra_methods()
        curr_percentage = method_catcher_repository.get_current_state_percentage()
        global progress_dialog
        if progress_dialog.value() >= 100:
            # schedule.clear()
            print("should stop method")
            return
        print("Running method. Percentage: " + str(curr_percentage))
        if progress_dialog.isVisible():
            progress_dialog.setValue(curr_percentage)
