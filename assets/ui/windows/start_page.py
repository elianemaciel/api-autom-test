from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel
import os

from assets.ui.util import style


class StartPageWidget:
    position = None
    instance = None

    @staticmethod
    def get_or_start(position=None):
        if StartPageWidget.position is None and position is None:
            raise ValueError("StartPageWidget not started yet. position has value 'None'. Please start the page first")
        if StartPageWidget.position is not None:
            return StartPageWidget.instance
        StartPageWidget.position = position
        StartPageWidget.instance = StartPageWidget._setup()
        return StartPageWidget.instance

    @staticmethod
    def _setup():
        start_page = QWidget()
        start_page_layout = QVBoxLayout()

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        start_page_layout.addItem(spacing)

        # Set application logo
        logo = QLabel()
        pixmap = QPixmap(os.path.join(os.getcwd(), 'ui/images/automtest-logo.png'))
        scaled_pixmap = pixmap.scaledToHeight(64)
        logo.setPixmap(scaled_pixmap)
        logo.resize(scaled_pixmap.width(), scaled_pixmap.height())
        logo.setAlignment(Qt.AlignCenter)
        start_page_layout.addWidget(logo)
        start_page.setLayout(start_page_layout)

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        start_page_layout.addItem(spacing)

        # Set main content
        program_description = QLabel()
        program_description.setText(mainScreenText())
        program_description.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        program_description.setWordWrap(True)
        start_page_layout.addWidget(program_description)

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        start_page_layout.addItem(spacing)

        return start_page


def mainScreenText():
        return """
Utilize o menu à esquerda para começar.


O AutomTest possui duas opções principais por onde começar: 


Inserindo uma História de Usuário ou Inserindo as informações dos métodos manualmente.


É só selecionar a opção correspondente no menu e continuar.
        """

