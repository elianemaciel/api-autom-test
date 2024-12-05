from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy

from assets.ui.util import color
from assets.ui.widgets.menu_button import AtMenuButton


class SuccessGeneratingTestsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: " + color.BACKGROUND + ";")
        self.setWindowTitle("Tests Generation")
        self.layout = QVBoxLayout()

        message = QLabel('Tests generated successfully.')
        message.setWordWrap(True)
        message.setStyleSheet("padding:10px; font-size: 16px;")
        self.layout.addWidget(message)
        # self.setFixedWidth(400)
        # self.setFixedHeight(100)
        self.setLayout(self.layout)
        self.setup_bottom_buttons()

    def setup_bottom_buttons(self):
        # Bottom button bar
        bottom_button_bar_layout = QHBoxLayout()
        spacing = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(spacing)

        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Okay",
                height=30,
                minimum_width=70,
                do_when_clicked=lambda: self.close(),
                btn_color=color.POPUP_BOTTOM_BUTTON_CANCEL
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)
        self.layout.addLayout(bottom_button_bar_layout)
