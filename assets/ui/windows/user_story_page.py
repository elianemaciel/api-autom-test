from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, \
    QMessageBox

from assets import StandardPlnRepository
from assets.AutomTestException import AutomTestException
from assets.ui.util import style
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.widgets.dialog.warning_errors_list_dialog import WarningErrorsListDialog


class InsertUserStoryWidget:
    position = None
    instance = None

    @staticmethod
    def get_or_start(position=None):
        if InsertUserStoryWidget.position is None and position is None:
            raise ValueError("UserStoryPageWidget not started yet. position has value 'None'. Please start the page "
                             "first")
        if InsertUserStoryWidget.position is not None:
            return InsertUserStoryWidget.instance
        InsertUserStoryWidget.position = position
        InsertUserStoryWidget.instance = InsertUserStoryWidget._setup()
        return InsertUserStoryWidget.instance

    @staticmethod
    def _setup():
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
        program_description.setText("Cole abaixo a história de usuário que você deseja converter:")
        program_description.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        program_description.setWordWrap(True)
        content_layout.addWidget(program_description)

        # Set text field
        user_story_text_edit = QTextEdit()
        user_story_text_edit.setStyleSheet("QTextEdit {border-radius: 10px; background-color: white}")
        content_layout.addWidget(user_story_text_edit)

        # Bottom button bar
        button_bar_layout = QHBoxLayout()

        spacing = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_bar_layout.addItem(spacing)

        # Set button bar
        button = AtMenuButton(
            text="Submeter História",
            height=30,
            minimum_width=170,
            do_when_clicked=lambda: submit_user_story(user_story_text_edit.toPlainText())
        )
        button_bar_layout.addWidget(button)

        content_layout.addLayout(button_bar_layout)

        # Set spacing
        # spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # content_layout.addItem(spacing)

        about_page.setLayout(content_layout)
        return about_page


def submit_user_story(user_story_data):
    # Aqui teremos a lógica de recuperar o campo com os dados do user story
    print("User story recebido: " + user_story_data)
    # E, em seguida, passamos para um repository responsável por enviar pro backend processar esse dado
    try:
        methods, warnings = StandardPlnRepository.send_user_story(user_story_data)
        warnings = [
            "This is the second warning, in which several things might have happened and must be treated"
            "First warning. Unable to retrieve the correct data from Given",
            "This is the second warning, in which several things might have happened and must be treated",
            "First warning. Unable to retrieve the correct data from Given",
            "This is the second warning, in which several things might have happened and must be treated",
            "First warning. Unable to retrieve the correct data from Given",
            "This is the second warning, in which several things might have happened and must be treated",
        ]
        methods = [#TODO: adicionar dados dentro do methods e ver a UO como confi
            "errorWhenClassAlreadyExists",
            "invalidClassName",
            "invalidClassNumber"
            "validClassNumber",
            "validClassName",
            "successWhenClassDoesNotExist",
            "classNameDefinitionSuccess",
            "interestOnClassName",
            "errorWhenClassAlreadyExists",
            "invalidClassName",
            "invalidClassNumber"
            "validClassNumber",
            "validClassName",
            "successWhenClassDoesNotExist",
            "classNameDefinitionSuccess",
            "interestOnClassName"
        ]
        if bool(warnings):
            cd = WarningErrorsListDialog(warnings, methods)
            cd.exec_()
        else:
            #Não aconteceram warnings. Ir para tela de resultado
            print("no warning. Complete success")
        # case continue, send to next screen: insert Methods info page
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


def show_message_dialog(mainText, icon, bttnsAndRoles, bodyText):
    # Create a QMessageBox instance
    popup = QMessageBox()
    popup.setWindowTitle("User Story Analysis")
    popup.setText(mainText)
    popup.setIcon(icon)
    for bttnsAndRole in bttnsAndRoles:
        popup.addButton(bttnsAndRole[0], bttnsAndRole[1])
    content_layout = QVBoxLayout()
    content_text = QLabel()
    content_text.setText(bodyText)
    content_text.setStyleSheet(style.BASIC_APPLICATION_TEXT)
    content_text.setWordWrap(True)
    content_layout.addWidget(content_text)
    popup.setLayout(content_layout)  # TODO: create a body of text to show every warning that occurred. What if lots happened?
    # Execute the popup and get the result
    result = popup.exec()
    print("message dialog exibido. Resultado é " + str(result))


def show_error_processing_user_story_message_dialog():
    show_message_dialog(
        "The User Story is ",
        QMessageBox.Information,
        [
            [AtMenuButton("Yes"), QMessageBox.YesRole],
            [AtMenuButton("No"), QMessageBox.NoRole],
            [AtMenuButton("Cancel"), QMessageBox.RejectRole],
        ],
        "Body text content 2"
    )
    # # Create a QMessageBox instance
    # popup = QMessageBox()
    # popup.setWindowTitle("User Story Analysis Error")
    # popup.setText("The User Story is ")
    # popup.setIcon(QMessageBox.Information)
    #
    # # Add buttons to the popup
    # # popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    # # popup.setDefaultButton(QMessageBox.Ok)
    #
    # # Add custom buttons
    # yes_button = AtMenuButton("Yes")
    # popup.addButton(yes_button, QMessageBox.YesRole)
    #
    # no_button = AtMenuButton("No")
    # popup.addButton(no_button, QMessageBox.NoRole)
    #
    # cancel_button = AtMenuButton("Cancel")
    # popup.addButton(cancel_button, QMessageBox.RejectRole)
    #
    # # Execute the popup and get the result
    # result = popup.exec()
    # print("message dialog exibido")
