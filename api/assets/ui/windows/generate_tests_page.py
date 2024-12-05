from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout, \
    QTextEdit

from assets.generator import generate_tests
from assets.ui.util import style, color
from assets.ui.widgets.dialog.success_generating_tests_dialog import SuccessGeneratingTestsDialog
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.windows.specify_equiv_class.specify_equiv_classes_page import SpecifyEquivClassesWidget


class GenerateTestsWidget:
    position = None
    instance = None
    # methods = []

    @staticmethod
    def get_or_start(position=None):
        if GenerateTestsWidget.position is None and position is None:
            raise ValueError("InsertMethodsInfo not started yet. position has value 'None'. Please start the page first")
        if GenerateTestsWidget.position is not None:
            return GenerateTestsWidget.instance
        GenerateTestsWidget.position = position
        GenerateTestsWidget.instance = GenerateTestsWidget._setup()
        return GenerateTestsWidget.instance

    @staticmethod
    def _setup():
        about_page = QWidget()
        content_layout = QVBoxLayout()

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        # Set application logo
        # logo = QLabel()
        # pixmap = QPixmap(os.path.join(os.getcwd(), 'ui/images/automtest-logo.png'))
        # scaled_pixmap = pixmap.scaledToHeight(64)
        # logo.setPixmap(scaled_pixmap)
        # logo.resize(scaled_pixmap.width(), scaled_pixmap.height())
        # logo.setAlignment(Qt.AlignCenter)
        # content_layout.addWidget(logo)


        # Set main content
        program_description = QLabel()
        program_description.setText("Choose a location to save the test files and generate the test files")
        program_description.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        program_description.setWordWrap(True)
        content_layout.addWidget(program_description)

        # Set spacing
        spacing = QSpacerItem(80, 80, QSizePolicy.Fixed, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        select_folder_layout = QHBoxLayout()
        name_text_edit = QTextEdit()
        name_text_edit.setStyleSheet("QTextEdit {border-radius: 10px; background-color: white}")
        # name_text_edit.setFixedWidth(320)
        name_text_edit.setFixedHeight(40)
        select_folder_layout.addWidget(name_text_edit)

        select_folder_layout.addWidget(AtMenuButton(
            text="Select location",
            height=40,
            maximum_width=150,
            minimum_width=150,
            btn_color=color.BOTTOM_NAVIGATION_FORWARD,
            do_when_clicked=lambda: name_text_edit.setText(GenerateTestsWidget.select_location(about_page))
        ))

        content_layout.addLayout(select_folder_layout)

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        btn_layout = QHBoxLayout()
        # btn_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        btn_layout.addWidget(AtMenuButton(
            text="Generate Tests",
            height=50,
            # maximum_width=300,
            # minimum_width=300,
            btn_color=color.ADD_NEW_METHOD_BUTTON,
            do_when_clicked=lambda: GenerateTestsWidget.generate_tests(name_text_edit.toPlainText())
        ))
        # btn_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        content_layout.addLayout(btn_layout)

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        about_page.setLayout(content_layout)
        return about_page

    @staticmethod
    def generate_tests(location):
        if location is None or location == "":
            print("Invalid Location")
        else:
            print("Generating tests in selected location")
            for i in range(0, len(SpecifyEquivClassesWidget.methods)):
                method = SpecifyEquivClassesWidget.methods[i][0]
                for testset in method.testsets:
                    testset.number_of_cases = int(testset.number_of_cases)
                generate_tests(method, file_path=location)
            SuccessGeneratingTestsDialog().exec_()

    @staticmethod
    def select_location(about_page):
        options = QFileDialog.Options()
        return QFileDialog.getExistingDirectory(about_page, "Select Folder to save your test cases", "",
                                                       options=options)
