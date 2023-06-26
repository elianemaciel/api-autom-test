from assets.qt_core import *
from assets.ui.util import color, style
from assets.ui.widgets.menu_button import AtMenuButton
import os

from assets.ui.windows.about_page import AboutPageWidget
from assets.ui.windows.check_inserted_data_page import CheckInsertedDataWidget
from assets.ui.windows.generate_tests_page import GenerateTestsWidget
from assets.ui.windows.insert_methods_info_page import InsertMethodsInfoWidget
from assets.ui.windows.specify_equiv_classes_page import SpecifyEquivClassesWidget
from assets.ui.windows.start_page import StartPageWidget
from assets.ui.windows.user_story_page import InsertUserStoryWidget


class UI_MainWindow(object):

    def __init__(self):
        self.menu_buttons = []

    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        # Set initial params
        parent.resize(960, 500)
        parent.setMinimumSize(960, 500)
        parent.setMaximumSize(960, 500)

        # Create central widget
        self.central_frame = QFrame()
        self.central_frame.setStyleSheet("background-color: " + color.BACKGROUND)

        # Create Main Layout
        self.main_layout = QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setupLeftMenu()

        # Add widgets to app
        self.main_layout.addWidget(self.left_menu)
        self.main_layout.addWidget(self.setupContentArea())

        # Set Central Widget
        parent.setCentralWidget(self.central_frame)

    def setupContentArea(self):
        content = QFrame()
        content.setStyleSheet("background-color: " + color.BACKGROUND)

        content_layout = QVBoxLayout()

        # Crio um QStackedWidget q contém todas as páginas
        self.all_pages = QStackedWidget()
        self.all_pages.addWidget(StartPageWidget.get_or_start(0))
        self.all_pages.addWidget(InsertUserStoryWidget.get_or_start(1))
        self.all_pages.addWidget(InsertMethodsInfoWidget.get_or_start(2))
        self.all_pages.addWidget(CheckInsertedDataWidget.get_or_start(3))
        self.all_pages.addWidget(SpecifyEquivClassesWidget.get_or_start(4))
        self.all_pages.addWidget(GenerateTestsWidget.get_or_start(5))
        self.all_pages.addWidget(AboutPageWidget.get_or_start(6))

        content_layout.addWidget(self.all_pages)
        content.setLayout(content_layout)

        return content

    def setupLeftMenu(self):
        self.left_menu = QFrame()
        self.left_menu.setStyleSheet("background-color: " + color.MENU_AREA)
        self.left_menu.setMaximumWidth(250)
        self.left_menu.setMinimumWidth(250)

        left_menu_layout = QVBoxLayout(self.left_menu)
        left_menu_layout.setContentsMargins(0, 0, 0, 0)
        left_menu_layout.setSpacing(0)

        # Area superior do menu, onde ficará a logo do programa
        left_menu_top_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        left_menu_layout.addItem(left_menu_top_spacer)

        # Set application logo
        self.logo = QLabel()
        pixmap = QPixmap(os.path.join(os.getcwd(), 'ui/images/automtest-logo.png'))
        scaled_pixmap = pixmap.scaledToHeight(38)
        self.logo.setPixmap(scaled_pixmap)
        self.logo.resize(scaled_pixmap.width(), scaled_pixmap.height())
        self.logo.setAlignment(Qt.AlignCenter)
        self.set_logo_visibility(False)
        left_menu_layout.addWidget(self.logo)


        # Top frame menu
        left_menu_top_frame = QFrame()
        left_menu_top_frame.setMinimumHeight(50)
        left_menu_top_frame.setObjectName("left_menu_top_frame")
        left_menu_top_frame.setStyleSheet("#left_menu_top_frame {background-color: " + color.MENU_AREA + "}")
        left_menu_top_frame.setContentsMargins(10, 10, 10, 10)

        left_menu_top_layout = QVBoxLayout(left_menu_top_frame)
        left_menu_top_layout.setContentsMargins(10, 10, 10, 10)
        left_menu_top_layout.setSpacing(20)

        # Buttons:
        btn_add_user_story = AtMenuButton(
            id="USER_STORY",
            text="Inserir uma História\nde Usuário",
            do_when_clicked=lambda: self.show_page(InsertUserStoryWidget.position, "USER_STORY")
        )
        # q_font = QFont()
        # q_font.setFamily("Arial")
        # q_font.setBold(300)
        # btn_add_user_story.setFont(q_font)
        btn_add_methods_info = AtMenuButton(
            id="INSERT_INFO",
            text="Inserir Informações\ndos Métodos",
            do_when_clicked=lambda: self.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")
        )
        btn_read_data = AtMenuButton(
            id="CHECK_DATA",
            text="Ver Dados Inseridos",
            do_when_clicked=lambda: self.show_page(CheckInsertedDataWidget.position, "CHECK_DATA")
        )
        btn_equiv_classes = AtMenuButton(
            id="EQUIV_CLASSES",
            text="Especificar Classes\nde Equivalência",
            do_when_clicked=lambda: self.show_page(SpecifyEquivClassesWidget.position, "EQUIV_CLASSES")
        )
        btn_generate_tests = AtMenuButton(
            id="TESTS",
            text="Gerar Testes",
            do_when_clicked=lambda: self.show_page(GenerateTestsWidget.position, "TESTS")
        )
        btn_about = AtMenuButton(
            id="ABOUT",
            text="Sobre o AutomTest",
            do_when_clicked=lambda: self.show_page(AboutPageWidget.position, "ABOUT")
        )

        # Add buttons to layout
        self.menu_buttons.append(btn_add_user_story)
        self.menu_buttons.append(btn_add_methods_info)
        self.menu_buttons.append(btn_read_data)
        self.menu_buttons.append(btn_equiv_classes)
        self.menu_buttons.append(btn_generate_tests)
        self.menu_buttons.append(btn_about)
        for btn in self.menu_buttons:
            left_menu_top_layout.addWidget(btn)

        # Add to layout
        left_menu_layout.addWidget(left_menu_top_frame)

    def show_page(self, position, id_button):
        self.set_logo_visibility(True)
        self.all_pages.setCurrentIndex(position)
        for btn in self.menu_buttons:
            btn.toggle_active(btn.id == id_button)

    def set_logo_visibility(self, is_visible):
        self.logo.setVisible(is_visible)
