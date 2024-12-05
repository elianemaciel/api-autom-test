import threading
import time
import traceback

from PySide6.QtCore import QTimer
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QProgressDialog, QVBoxLayout, QLabel

from assets.repository.MultiMethodCatcherRepository import MultiMethodCatcherRepository
from assets.ui.util import color

lock = threading.Lock()
while_lock = threading.Lock()
fin_exec_lock = threading.Lock()
# progress_dialog = None
llm_execution_thread = None
dialog = None

# method_catcher_repository = LLMRepository
# method_catcher_repository = PalmLlmRepository()
# method_catcher_repository = NlpRepository()
method_catcher_repository = MultiMethodCatcherRepository()
is_fin_exec = False


# class DialogWorker(QThread):
#
#     def __init__(self, after_rendered):
#         super().__init__()
#         self.after_rendered = after_rendered
#
#     def run(self):
#         dialog = NonBlockingDialog(self.after_rendered)
#         dialog.exec()


# class LoadingDialog(QDialog):
class LoadingDialog(QProgressDialog):
    def __init__(self, after_rendered):
        super().__init__()
        self.setRange(0, 0)  # Set range to indeterminate
        self.setModal(True)

        # self.setWindowTitle("Non-blocking Dialog")
        self.after_rendered = after_rendered
        #
        # layout = QVBoxLayout()
        #
        # label = QLabel("This is a non-blocking dialog")
        # layout.addWidget(label)
        #
        # close_button = QPushButton("Close")
        # close_button.clicked.connect(self.close)
        # layout.addWidget(close_button)
        #
        # self.setLayout(layout)
        self.setStyleSheet("background-color: " + color.BACKGROUND + ";")
        self.setWindowTitle("Methods suggestions")
        self.layout = QVBoxLayout()

        # self.progress_bar = QProgressBar()
        # self.progress_bar.setRange(0, 0)  # Set range to indeterminate
        # self.progress_bar.setStyleSheet("QProgressBar {"
        #                                 "border: none;"
        #                                 "text-align: center;"
        #                                 "background-color: transparent;"
        #                                 "}"
        #                                 "QProgressBar::chunk {"
        #                                 "background-color: #2196F3;"  # Blue color
        #                                 "}")
        # self.layout.addWidget(self.progress_bar)

        message1 = QLabel("Generating methods suggestions")
        message2 = QLabel("This might take a few moments. Please wait.")
        message1.setWordWrap(True)
        message2.setWordWrap(True)
        message1.setStyleSheet("padding:10px; font-size: 16px;")
        message2.setStyleSheet("padding:10px; font-size: 16px;")
        self.layout.addWidget(message1)
        self.layout.addWidget(message2)
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.setLayout(self.layout)

        # Set dialog attributes for non-modal behavior
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModality.NonModal)

        # self.showEvent = lambda event: self.on_show_event(event)

        QTimer.singleShot(100, self.after_rendered)

    # def on_show_event(self, event):
    #     print('Prestes a executar')
    #     self.after_rendered()


# def load_dialog():
#     dialog = LoadingMethodsSuggestion(lambda: hasFinishedExecution())
#     dialog.exec_()
#
#
# def schedule_load_dialog(scheduler_thread):
#     scheduler_thread.every().second.do(load_dialog)
#     # dialog = LoadingMethodsSuggestion(lambda: hasFinishedExecution())
#     # dialog.exec_()
#     # scheduler_thread.run_pending()
#     while True:
#         try:
#             scheduler_thread.run_pending()
#         except Exception as e:
#             print(e)
#             pass
#         time.sleep(1)


# def hasFinishedExecution():
#     with fin_exec_lock:
#         global is_fin_exec
#         return is_fin_exec




def run_and_close_dialog():
    _run_llm()
    dialog.close()


def run(user_story_txt, language, parent=None):
    # global llm_execution_thread, progress_dialog

    method_catcher_repository.setup(user_story_txt, language)

    # scheduler_thread = schedule.Scheduler()
    # llm_execution_thread = threading.Thread(target=_run_llm)
    # llm_execution_thread = threading.Thread(target=_run_llm)
    # llm_execution_thread.setDaemon(True)
    # llm_execution_thread.start()
    # scheduler_thread.clear()
    # scheduler_thread = schedule.Scheduler()
    # job_thread = threading.Thread(target=schedule_load_dialog, args=(scheduler_thread,))
    # job_thread.setDaemon(True)
    # job_thread.start()
    global dialog
    dialog = LoadingDialog(run_and_close_dialog)
    dialog.exec()

    # _run_llm()

    # scheduler_thread.clear()



    # progress_dialog = QProgressDialog("Generating method suggestions...", "Abort Generation", 0, 100)
    # parent.addWidget(progress_dialog)
    # progress_dialog.resize(400, 200)
    # progress_dialog.setWindowTitle("Method suggestions")
    # icon = QIcon("../img/logo.jpg")  # Replace with the path to your icon file
    # progress_dialog.setWindowIcon(icon)
    # progress_dialog.exec_()

    # llm_execution_thread.join()

    # time.sleep(5)
    return method_catcher_repository.get_caught_methods()


def _run_llm():
    # schedule.every().do(_update_methods_result_and_percentage)
    # while LLMRepository.get_current_state_percentage() < 100:
    while True:
        print('entrou no while')
        with while_lock:
            _update_methods_result_and_percentage()
            print('entrou no while_lock')
            if method_catcher_repository.get_current_state_percentage() >= 100:
                break
            try:
                print("running pending")
                # schedule.run_pending()
            except Exception as e:
                traceback.print_exc()
                print("Error while getting extra methods suggestions from user story: " + e.__str__())
            time.sleep(1)
    # schedule.clear()
    print('Exited _run_llm')


def _update_methods_result_and_percentage():
    with lock:
        print("_update_methods_result_and_percentage start")
        # LLMRepository.get_extra_suggestions_from_user_story()
        method_catcher_repository.compute_extra_methods()
        curr_percentage = method_catcher_repository.get_current_state_percentage()
        # global progress_dialog
        if curr_percentage >= 100:
            # schedule.clear()
            print("should stop method")
            return
        print("Running method. Percentage: " + str(curr_percentage))
        #if progress_dialog.isVisible():
        #    progress_dialog.setValue(curr_percentage)
