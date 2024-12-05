from PySide6.QtWidgets import QHBoxLayout, QCheckBox, QLabel

from assets.ui.util import color
from assets.ui.widgets.menu_button import AtMenuButton


class MethodCrud(QHBoxLayout):
    def __init__(self,
                 method,
                 do_when_edit_is_clicked=None,
                 do_when_remove_is_clicked=None,
                 is_active=True
                 ):
        super().__init__()
        self.is_active = is_active
        self.method_info = method

        # Text label with info
        item_description = QLabel("<html><b>Method: </b> " + self.method_info.name + "</html>")
        item_description.setStyleSheet("""
                               QLabel {
                                   border-radius: 10px; 
                                   background-color: white; 
                                   padding:10px;
                                   font-family: Arial; 
                                   font-size: 14px;
                                   height: 30px,
                               }
                               """)
        # item_description.setWordWrap(True)
        self.addWidget(item_description)

        # Edit button
        edit_bttn = AtMenuButton(
            text="Edit",
            height=40,
            minimum_width=70,
            maximum_width=70,
            btn_color=color.EDIT_BUTTON,
            do_when_clicked=do_when_edit_is_clicked
        )
        self.addWidget(edit_bttn)

        #Remove button
        remove_bttn = AtMenuButton(
            text="Remove",
            height=40,
            minimum_width=80,
            maximum_width=80,
            btn_color=color.REMOVE_BUTTON,
            do_when_clicked=do_when_remove_is_clicked
        )
        self.addWidget(remove_bttn)

    def is_checkbox_selected(self):
        return self.item_checkbox.isChecked()

    def get_method_info(self):
        return self.method_info

