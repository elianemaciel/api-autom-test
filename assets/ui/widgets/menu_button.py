from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPushButton, QToolButton

from assets.ui.util import color


class AtMenuButton(QPushButton):
    def __init__(
            self,
            id="",
            text="",
            height=50,
            minimum_width=50,
            maximum_width=None,
            text_padding=55,
            text_color=color.MENU_BUTTON_TEXT,
            btn_color=color.MENU_BUTTON_BACKGROUND,
            btn_hover=color.MENU_BUTTON_HOVER,
            btn_pressed=color.MENU_BUTTON_PRESSED,
            is_active=False,
            do_when_clicked=None
    ):
        super().__init__()

        # set default params
        self.setText(text)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height),
        self.setMinimumWidth(minimum_width)
        if maximum_width is not None:
            self.setMaximumWidth(maximum_width)
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(  # //lambda: (
            do_when_clicked  # ,
            # self.toggle_active(True),
            # )
        )
        self.id = id
        # self.text_padding = 20

        # Custom parameters
        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.text_color = text_color
        self.btn_color = btn_color
        self.btn_hover = btn_hover
        self.btn_pressed = btn_pressed
        self.is_active = is_active

        self.set_style(
            self.text_padding,
            self.text_color,
            self.btn_color,
            self.btn_hover,
            self.btn_pressed,
            self.is_active
        )

    def toggle_active(self, is_active):
        self.is_active = is_active
        # self.is_active = not self.is_active
        self.set_style(
            self.text_padding,
            self.text_color,
            self.btn_color,
            self.btn_hover,
            self.btn_pressed,
            self.is_active
        )

    def set_style(
            self,
            text_padding=55,
            text_color=color.MENU_BUTTON_TEXT,
            btn_color=color.MENU_BUTTON_BACKGROUND,
            btn_hover=color.MENU_BUTTON_HOVER,
            btn_pressed=color.MENU_BUTTON_PRESSED,
            is_active=False
    ):
        style = f"""
        QPushButton {{
            color: {text_color};
            background-color: {btn_color};
            font-size: 12pt;
            text-align: center;
            border: none;
            border-radius: 10;
            text-padding: 55;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background-color: {btn_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_pressed};
        }}
        """

        active_style = f"""
        QPushButton {{
            background-color: {color.MENU_BUTTON_ACTIVE};
        }}
        """

        if is_active:
            self.setStyleSheet(style + active_style)
        else:
            self.setStyleSheet(style)

        # self.setFont(QFont("Monospace"))
