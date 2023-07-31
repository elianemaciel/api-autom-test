from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, \
    QTextEdit

from assets.components import Parameter, ParamRange
from assets.ui.util import color
from assets.ui.widgets.combo_box import CustomComboBox
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.widgets.param_edit_item import ParamEditItem


class EquivalenceClassParamsDialog(QDialog):
    def __init__(self, param_list, equiv_class_name, parent=None):
        super().__init__(parent)

        self.setFixedWidth(600)
        self.setFixedHeight(300)
        self.current_params_list = param_list

        self.setStyleSheet("background-color: " + color.BACKGROUND + ";")
        self.setWindowTitle("Set parameter ranges or equivalence class")
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
        # equiv_class_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
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

        # Param range-----------------------------------------------------------------------------------
        label = QLabel("Building parameter range for parameter " + param_list[0] + ":")
        label.setFixedHeight(30)
        label.setStyleSheet("font-family: Arial;  font-size: 14px;")
        self.layout.addWidget(label)

        scroll = QScrollArea()
        scroll.setFixedHeight(117)
        # scroll.setFixedWidth(420)
        params = QHBoxLayout()
        params.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollContent.setFixedHeight(100)
        scrollLayout = QHBoxLayout(scrollContent)
        scroll.setWidget(scrollContent)
        scroll.setStyleSheet("border: none;")
        param_ranges = [ParamRange(param_list[0], "[-][numbers][.]", "[0~1][1~4][0~1]")]
        for param_range in param_ranges:

            param_widget = QWidget()
            param_widget.setFixedHeight(70)
            param_widget.setStyleSheet("border-radius: 10px; background-color: " + color.LIGHT_GRAY + ";")

            param_layout = QVBoxLayout()

            label = QLabel("Substring:")
            label.setStyleSheet(
                "font-family: Arial; "
                "font-size: 14px;")
            param_layout.addWidget(label)

            label = QLabel("Quantity:")
            label.setStyleSheet(
                "font-family: Arial; "
                "font-size: 14px;")
            param_layout.addWidget(label)
            param_widget.setLayout(param_layout)
            scrollLayout.addWidget(param_widget)

            for i in range(0, param_range.amount_of_elements()):
                curr_substr, curr_range = param_range.get_range_by_index(i)
                curr_range_start = curr_range.split("~")[0]
                curr_range_end = curr_range.split("~")[1]

                param_widget = QWidget()
                param_widget.setFixedHeight(70)
                param_widget.setStyleSheet("border-radius: 10px; background-color: " + color.LIGHT_GRAY + ";")

                param_layout = QVBoxLayout()
                # param_layout.setAlignment(Qt.AlignCenter)

                # substring
                label = QLabel(curr_substr)
                label.setStyleSheet(
                    "padding: 5px; "
                    "font-family: Arial; "
                    "font-size: 14px; "
                    "border-radius: 5px; "
                    "background-color: white;")
                label.setAlignment(Qt.AlignCenter)
                param_layout.addWidget(label)

                # quantity
                quantity_layout = QHBoxLayout()
                label = QLabel(curr_range_start)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(
                    "padding:2px; font-family: Arial; font-size: 14px; border-radius: 5px; background-color: white;")
                quantity_layout.addWidget(label)

                label = QLabel("to")
                label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px;")
                quantity_layout.addWidget(label)

                label = QLabel(curr_range_end)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(
                    "padding:2px; font-family: Arial; font-size: 14px; border-radius: 5px; background-color: white;")
                quantity_layout.addWidget(label)

                param_layout.addLayout(quantity_layout)

                param_widget.setLayout(param_layout)
                scrollLayout.addWidget(param_widget)

            scrollLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            scrollLayout.addWidget(AtMenuButton(
                text="Add more",
                height=70,
                minimum_width=70,
                font_size=10,
                btn_color=color.ADD_NEW_METHOD_BUTTON
            ))

        self.layout.addLayout(params)
        self.setup_bottom_buttons()

        self.setLayout(self.layout)

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
                    # PageManager.show_insert_methods_info_success(methods),
                    self.close()
                ),
                btn_color=color.POPUP_BOTTOM_BUTTON_OK
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)
        self.layout.addLayout(bottom_button_bar_layout)
