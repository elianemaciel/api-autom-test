from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout

from assets.AutomTestException import AutomTestException
from assets.ui import LoadingPopupManager
from assets.ui.util import style
from assets.ui.widgets.RadioButton import RadioButton
from assets.ui.widgets.dialog.warning_errors_list_dialog import WarningErrorsListDialog
from assets.ui.widgets.menu_button import AtMenuButton

methods = None
warnings = None


class InsertUserStoryWidget:
    position = None
    instance = None
    language_radio_btn = None

    @staticmethod
    def get_or_start(do_to_show_insert_methods_info_success, position=None):
        if InsertUserStoryWidget.position is None and position is None:
            raise ValueError("UserStoryPageWidget not started yet. position has value 'None'. Please start the page "
                             "first")
        if InsertUserStoryWidget.position is not None:
            return InsertUserStoryWidget.instance
        InsertUserStoryWidget.position = position
        InsertUserStoryWidget.instance = InsertUserStoryWidget._setup(do_to_show_insert_methods_info_success)
        return InsertUserStoryWidget.instance

    @staticmethod
    def _setup(do_to_show_insert_methods_info_success):
        about_page = QWidget()
        content_layout = QVBoxLayout()

        # # Set spacing
        # spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # content_layout.addItem(spacing)

        # Set spacing
        spacing = QSpacerItem(50, 60, QSizePolicy.Minimum, QSizePolicy.Minimum)
        content_layout.addItem(spacing)

        # Set description if textFiled
        program_description = QLabel()
        program_description.setText("Paste below the User Story you want to convert:")
        program_description.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        program_description.setWordWrap(True)
        content_layout.addWidget(program_description)

        # Set text field
        user_story_text_edit = QTextEdit()
        user_story_text_edit.setStyleSheet("QTextEdit {border-radius: 10px; background-color: white}")
        content_layout.addWidget(user_story_text_edit)

        # Bottom button bar
        button_bar_layout = QHBoxLayout()

        InsertUserStoryWidget.language_radio_btn = RadioButton("Português", "English")
        button_bar_layout.addWidget(InsertUserStoryWidget.language_radio_btn)

        spacing = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_bar_layout.addItem(spacing)

        # Set button bar
        button = AtMenuButton(
            text="Submit Story",
            height=30,
            minimum_width=170,
            do_when_clicked=lambda: submit_user_story(
                user_story_text_edit.toPlainText(),
                do_to_show_insert_methods_info_success,
                content_layout
            )
        )
        button_bar_layout.addWidget(button)

        content_layout.addLayout(button_bar_layout)

        # Set spacing
        # spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # content_layout.addItem(spacing)

        about_page.setLayout(content_layout)
        return about_page


# def send_user_story_to_llm(user_story_data, progress):
#     global methods, warnings
#     methods, warnings = LLMRepository.send_user_story(
#         user_story_data,
#         7,
#         lambda rep: progress.setValue(rep)
#     )
#
#
# def send_user_story_to_llm(user_story_data):
#     global methods, warnings
#     methods, warnings = LLMRepository.send_user_story(user_story_data, 7)


def get_curr_selected_language_acronym():
    if InsertUserStoryWidget.language_radio_btn.get_selected() == "Português":
        return "pt"
    return "en"


def submit_user_story(user_story_data, do_to_show_insert_methods_info_success, parent_layout):
    # Aqui teremos a lógica de recuperar o campo com os dados do user story
    # E, em seguida, passamos para um repository responsável por enviar pro backend processar esse dado
    try:
        # progress = QProgressDialog("Generating method suggestions...", "Abort Generation", 0, 4)
        # parent_layout.addWidget(progress)
        # progress.setWindowModality(Qt.ApplicationModal)
        # QTimer.singleShot(100, lambda: send_user_story_to_llm(user_story_data, progress))
        # progress.exec_()

        # progressDialog = LlmResolutionProgressDialog(lambda progress: send_user_story_to_llm(user_story_data, progress))
        # progressDialog.exec()

        # progress = LlmResolutionProgressDialog2("Generating method suggestions...", "Abort Generation", 0, 4)
        # progress = LlmResolutionProgressDialog(lambda progress_: send_user_story_to_llm(user_story_data, progress_))
        # progress.setWindowModality(Qt.ApplicationModal)

        # progress.exec_()#TODO: colocar para executar em outra thread e ir inserindo os updates para o progresso
        # QTimer.singleShot(10, lambda: send_user_story_to_llm(user_story_data, progress))
        global methods
        methods = LoadingPopupManager.run(user_story_data, get_curr_selected_language_acronym(), parent_layout)

        if bool(warnings):
            cd = WarningErrorsListDialog(do_to_show_insert_methods_info_success, warnings, methods)
            cd.exec_()
        else:
            #Não aconteceram warnings. Ir para tela de resultado
            do_to_show_insert_methods_info_success(methods)

    except AutomTestException as e:
        # Show error message in popup
        print(e.message)
    except Exception as e2:
        # show "Internal error occurred. Logs can be accessed <place>" in popup
        print(e2)
    # O repository deve retornar algo que utilizaremos para mostrar na tela:
    #  (1) Uma negativa, com uma causa
    #  (2) Os dados necessários que passaremos para a próxima página
    # show_error_processing_user_story_message_dialog()
