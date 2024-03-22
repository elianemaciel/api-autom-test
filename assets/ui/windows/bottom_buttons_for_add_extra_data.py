from PySide6.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy

from assets.ui.util import color
from assets.ui.widgets.menu_button import AtMenuButton


class BottomButtonsForAddExtraData(QHBoxLayout):
    def __init__(self, do_to_show_next_page, do_to_go_back):
        super().__init__()

        spacing = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.addItem(spacing)
        self.addWidget(
            AtMenuButton(
                text="Go Back",
                # height=30,
                minimum_width=100,
                do_when_clicked=do_to_go_back,
                btn_color=color.BOTTOM_NAVIGATION_BACKWARD
            )
        )
        self.addWidget(
            AtMenuButton(
                text="Continue",
                minimum_width=170,
                do_when_clicked=do_to_show_next_page,
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.addItem(end_spacing)

