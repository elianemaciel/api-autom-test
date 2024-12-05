from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget

from assets.ui.util import color
from assets.ui.widgets.menu_button import AtMenuButton


class WarningErrorsListDialog(QDialog):
    def __init__(self, do_to_show_insert_methods_info_success, warnings_and_errors, methods, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: " + color.BACKGROUND + ";")
        self.setWindowTitle("Warnings when converting User Story")
        self.layout = QVBoxLayout()

        message = QLabel("Some warnings occurred when converting User Stories:")
        message.setStyleSheet("padding:10px; font-size: 14px;")
        self.layout.addWidget(message)
        self.setFixedWidth(600)
        self.setFixedHeight(300)

        #Create scroll area to show errors and warnings:
        scroll = QScrollArea()
        self.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scroll.setWidget(scrollContent)
        scroll.setStyleSheet("border: none;")
        for item in warnings_and_errors:
            label = QLabel(item)
            label.setStyleSheet("""
            QLabel {
                border-radius: 10px; 
                background-color: white; 
                padding:10px;
                font-family: Arial; 
                font-size: 14px;
            }
            """)
            label.setWordWrap(True)

            scrollLayout.addWidget(label)

        self.setLayout(self.layout)
        self.setup_bottom_buttons(do_to_show_insert_methods_info_success, methods)

    def setup_bottom_buttons(self, do_to_show_insert_methods_info_success, methods):
        # Bottom button bar
        bottom_button_bar_layout = QHBoxLayout()
        spacing = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(spacing)
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Ignore and Continue",
                height=30,
                minimum_width=170,
                do_when_clicked=lambda: (
                    do_to_show_insert_methods_info_success(methods),
                    self.close()
                ),
                btn_color=color.POPUP_BOTTOM_BUTTON_OK
            )
        )
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Cancel",
                height=30,
                minimum_width=70,
                do_when_clicked=lambda: self.close(),
                btn_color=color.POPUP_BOTTOM_BUTTON_CANCEL
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)
        self.layout.addLayout(bottom_button_bar_layout)
