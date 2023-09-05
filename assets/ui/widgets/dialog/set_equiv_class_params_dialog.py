from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget

from assets.ui.layouts.StringRangeLayout import StringRangeLayout
from assets.ui.util import color
from assets.ui.widgets.menu_button import AtMenuButton


class EquivalenceClassParamsDialog(QDialog):
    def __init__(self, param_ranges, equiv_class_name, parent=None):
        super().__init__(parent)

        self.string_range_layouts = []

        self.setFixedWidth(800)
        self.setFixedHeight(500)
        self.current_param_range_list = param_ranges
        self.equiv_class_name = equiv_class_name
        self.parent = parent

        self.setStyleSheet("background-color: " + color.BACKGROUND + ";")
        self.setWindowTitle("Set parameter ranges or equivalence class")
        self.setup_all_view(equiv_class_name, param_ranges)

    def setup_all_view(self, equiv_class_name, param_ranges):
        self.layout = QVBoxLayout()
        message = QLabel("Define parameter ranges for equivalence class:")
        message.setStyleSheet("padding:10px; font-size: 14px;")
        message.setFixedHeight(40)
        message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(message)
        # Equiv class-------------------------------------------------------------------------------
        equiv_class_layout = QHBoxLayout()
        label = QLabel("Equivalence class:")
        label.setFixedHeight(40)
        label.setFixedWidth(170)
        label.setStyleSheet("""
            QLabel {
                padding:10px;
                font-family: Arial; 
                font-size: 14px;
                font-weight: bold;
            }
        """)
        equiv_class_layout.addWidget(label)
        label = QLabel(equiv_class_name)
        label.setFixedHeight(40)
        label.setStyleSheet("""
            QLabel {
                border-radius: 10px; 
                background-color: """ + color.LIGHT_GRAY + """; 
                padding:10px;
                font-family: Arial; 
                font-size: 14px;
            }
        """)
        equiv_class_layout.addWidget(label)
        self.layout.addLayout(equiv_class_layout)
        self.setup_parameter_range_views(param_ranges)
        self.setLayout(self.layout)

    def setup_parameter_range_views(self, param_ranges):
        # Param range-----------------------------------------------------------------------------------

        vertical_scroll = QScrollArea()
        self.layout.addWidget(vertical_scroll)
        vertical_scroll.setWidgetResizable(True)
        vertical_scroll_content = QWidget(vertical_scroll)
        vertical_scroll_layout = QVBoxLayout(vertical_scroll_content)
        vertical_scroll.setWidget(vertical_scroll_content)
        vertical_scroll.setStyleSheet("border: none;")

        for param_range in param_ranges:

            string_range_layout = StringRangeLayout(param_range)
            self.string_range_layouts.append(string_range_layout)
            vertical_scroll_layout.addLayout(string_range_layout)

        self.setup_bottom_buttons()

    def setup_bottom_buttons(self):
        # Bottom button bar
        bottom_button_bar_layout = QHBoxLayout()
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Help",
                height=30,
                minimum_width=90,
                do_when_clicked=lambda: self.close(),
                btn_color=color.BOTTOM_NAVIGATION_LIST_ALL
            )
        )
        bottom_button_bar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Cancel",
                height=30,
                minimum_width=90,
                do_when_clicked=lambda: self.close(),
                btn_color=color.POPUP_BOTTOM_BUTTON_CANCEL
            )
        )
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Save",
                height=30,
                minimum_width=90,
                do_when_clicked=lambda: (
                    self.update_current_param_range_list(),
                    self.close()
                ),
                btn_color=color.POPUP_BOTTOM_BUTTON_OK
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)
        self.layout.addLayout(bottom_button_bar_layout)

    def update_current_param_range_list(self):
        #TODO: verify data before saving

        for i in range(0, len(self.string_range_layouts)):
            srl = self.string_range_layouts[i]
            content, quantity = srl.get_range_data()
            self.current_param_range_list[i].v1 = content
            self.current_param_range_list[i].v2 = quantity
