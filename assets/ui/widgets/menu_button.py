import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

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
            font_size=12,
            border_radius=10,
            text_color=color.MENU_BUTTON_TEXT,
            btn_color=color.MENU_BUTTON_BACKGROUND,
            btn_hover=color.MENU_BUTTON_HOVER,
            btn_pressed=color.MENU_BUTTON_PRESSED,
            is_active=False,
            is_clickable=True,
            do_when_clicked=None
    ):
        super().__init__()

        # set default params
        self.setText(text)
        if height is not None:
            self.setMaximumHeight(height)
            self.setMinimumHeight(height)
        self.setMinimumWidth(minimum_width)
        if maximum_width is not None:
            self.setMaximumWidth(maximum_width)
        self.setCursor(Qt.PointingHandCursor)
        self.setup_on_click(do_when_clicked)
        self.id = id
        self.font_size = font_size
        self.is_clickable = is_clickable
        # self.text_padding = 20

        # Custom parameters
        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.text_color = text_color
        self.btn_color = btn_color
        self.btn_hover = btn_hover
        self.btn_pressed = btn_pressed
        self.border_radius = border_radius
        self.is_active = is_active

        self.set_style(
            self.text_padding,
            self.text_color,
            self.btn_color,
            self.btn_hover,
            self.btn_pressed,
            self.font_size,
            self.border_radius,
            self.is_active,
            self.is_clickable
        )

    def setup_on_click(self, do_when_clicked):
        self.clicked.connect(do_when_clicked)

    def toggle_active(self, is_active):
        # print("toggle_active: " + str(is_active) + " ID: " + self.id)
        self.is_active = is_active
        self.set_style(
            self.text_padding,
            self.text_color,
            self.btn_color,
            self.btn_hover,
            self.btn_pressed,
            self.font_size,
            self.border_radius,
            self.is_active,
            self.is_clickable
        )

    def toggle_clickable(self, is_clickable):
        # print("toggle_clickable: " + str(is_clickable) + " ID: " + self.id)
        self.is_clickable = is_clickable
        self.setEnabled(is_clickable)
        self.set_style(
            self.text_padding,
            self.text_color,
            self.btn_color,
            self.btn_hover,
            self.btn_pressed,
            self.font_size,
            self.border_radius,
            self.is_active,
            self.is_clickable
        )

    def set_style(
            self,
            text_padding=55,
            text_color=color.MENU_BUTTON_TEXT,
            btn_color=color.MENU_BUTTON_BACKGROUND,
            btn_hover=color.MENU_BUTTON_HOVER,
            btn_pressed=color.MENU_BUTTON_PRESSED,
            font_size=12,
            border_radius=10,
            is_active=False,
            is_clickable=True
    ):
        style = f"""
        QPushButton {{
            color: {text_color};
            background-color: {btn_color};
            font-size: {font_size}pt;
            text-align: center;
            border: none;
            border-radius: {border_radius};
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

        not_clickable_style = f"""
        QPushButton {{
            background-color: {color.MENU_BUTTON_NOT_CLICKABLE};
        }}
        QPushButton:hover {{
            background-color: {color.MENU_BUTTON_NOT_CLICKABLE};
        }}
        QPushButton:pressed {{
            background-color: {color.MENU_BUTTON_NOT_CLICKABLE};
        }}
        """

        if not is_clickable:
            self.setStyleSheet(style + not_clickable_style)
        elif is_active:
            self.setStyleSheet(style + active_style)
        else:
            self.setStyleSheet(style)
        self.update()
