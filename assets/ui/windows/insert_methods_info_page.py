from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel
import os

from assets.ui.util import style


class InsertMethodsInfoWidget:
    position = None
    instance = None

    @staticmethod
    def get_or_start(position=None):
        if InsertMethodsInfoWidget.position is None and position is None:
            raise ValueError("InsertMethodsInfo not started yet. position has value 'None'. Please start the page first")
        if InsertMethodsInfoWidget.position is not None:
            return InsertMethodsInfoWidget.instance
        InsertMethodsInfoWidget.position = position
        InsertMethodsInfoWidget.instance = InsertMethodsInfoWidget._setup()
        return InsertMethodsInfoWidget.instance

    @staticmethod
    def _setup():
        about_page = QWidget()
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
        program_description.setText("Content for Insert Methods Info page")
        program_description.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        program_description.setWordWrap(True)
        content_layout.addWidget(program_description)

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        about_page.setLayout(content_layout)
        return about_page
