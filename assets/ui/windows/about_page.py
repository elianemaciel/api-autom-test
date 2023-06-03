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
        content_widget = QWidget()
        content_layout = QVBoxLayout()

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        # Set application logo
        logo = QLabel()
        pixmap = QPixmap(os.path.join(os.getcwd(), 'ui/images/automtest-logo.png'))
        scaled_pixmap = pixmap.scaledToHeight(64)
        logo.setPixmap(scaled_pixmap)
        logo.resize(scaled_pixmap.width(), scaled_pixmap.height())
        logo.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(logo)

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        # Set main content
        program_description = QLabel()
        program_description.setText("Content for about page")
        program_description.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        program_description.setWordWrap(True)
        content_layout.addWidget(program_description)

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        content_widget.setLayout(content_layout)
        return content_widget
