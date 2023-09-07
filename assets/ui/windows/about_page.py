from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel
import os

from assets.ui.util import style


class AboutPageWidget:
    position = None
    instance = None

    @staticmethod
    def get_or_start(position=None):
        if AboutPageWidget.position is None and position is None:
            raise ValueError("AboutPageWidget not started yet. position has value 'None'. Please start the page first")
        if AboutPageWidget.position is not None:
            return AboutPageWidget.instance
        AboutPageWidget.position = position
        AboutPageWidget.instance = AboutPageWidget._setup()
        return AboutPageWidget.instance

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
Use the left menu to start.

AutomTest has two main options for you to start with:

1. Inserting an User Story
2. Inserting the Methods Information manually

Select the corresponding option in the left menu and continue
        """
