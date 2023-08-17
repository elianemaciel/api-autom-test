from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, \
    QLineEdit

from assets.ui.util import color
from assets.ui.widgets.combo_box import CustomComboBox
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.widgets.param_range_add_button import ParamRangeAddButton


class EquivalenceClassParamsDialog(QDialog):
    def __init__(self, param_ranges, equiv_class_name, parent=None):
        super().__init__(parent)

        self.horizontal_scroll_layouts = []
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

            full_param_def_layout = QVBoxLayout()
            label = QLabel("Building parameter range for parameter <b>" + param_range.param + "</b>:")
            # label.setFixedHeight(30)
            label.setStyleSheet("font-family: Arial;  font-size: 14px;")
            full_param_def_layout.addWidget(label)

            param_def_layout = QHBoxLayout()
            full_param_def_layout.addLayout(param_def_layout)

            horizontal_scroll = QScrollArea()
            horizontal_scroll.setFixedHeight(137)
            horizontal_scroll.setWidgetResizable(True)
            horizontal_scroll_content = QWidget(horizontal_scroll)
            horizontal_scroll_content.setFixedHeight(120)
            horizontal_scroll_layout = QHBoxLayout(horizontal_scroll_content)
            horizontal_scroll.setWidget(horizontal_scroll_content)
            horizontal_scroll.setStyleSheet("border: none;")
            self.horizontal_scroll_layouts.append(horizontal_scroll_layout)


            param_widget = QWidget()
            param_widget.setFixedHeight(100)
            param_widget.setStyleSheet("border-radius: 10px; background-color: " + color.LIGHT_GRAY + ";")

            param_label_layout = QVBoxLayout()

            label = QLabel("Type:")
            label.setStyleSheet("font-family: Arial; font-size: 14px;")
            param_label_layout.addWidget(label)

            label = QLabel("Content:")
            label.setStyleSheet("font-family: Arial; font-size: 14px;")
            param_label_layout.addWidget(label)

            label = QLabel("Quantity:")
            label.setStyleSheet("font-family: Arial; font-size: 14px;")
            param_label_layout.addWidget(label)

            param_widget.setLayout(param_label_layout)
            param_label_wrapper_layout = QVBoxLayout()
            param_label_wrapper_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed))
            param_label_wrapper_layout.addWidget(param_widget)
            param_label_wrapper_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
            param_def_layout.addLayout(param_label_wrapper_layout)

            param_def_layout.addWidget(horizontal_scroll)

            for i in range(0, param_range.amount_of_elements()):
                curr_substr, curr_range = param_range.get_range_by_index(i)
                curr_range_start = curr_range.split("~")[0]
                curr_range_end = curr_range.split("~")[1]

                horizontal_scroll_layout.addWidget(self.build_param_range_element(curr_range_end, curr_range_start, curr_substr))

            horizontal_scroll_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

            param_label_wrapper_layout = QVBoxLayout()
            param_label_wrapper_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed))
            param_label_wrapper_layout.addWidget(ParamRangeAddButton(
                id=self.horizontal_scroll_layouts.index(horizontal_scroll_layout),
                text="Add\nmore",
                height=100,
                minimum_width=70,
                font_size=10,
                btn_color=color.ADD_NEW_METHOD_BUTTON,
                do_when_clicked=lambda layout_id: self.add_more_on_click(layout_id)
            ))
            param_label_wrapper_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
            param_def_layout.addLayout(param_label_wrapper_layout)
            vertical_scroll_layout.addLayout(full_param_def_layout)

        self.setup_bottom_buttons()

    def add_more_on_click(self, curr_index):
        print("Add more to " + str(curr_index))
        return self.horizontal_scroll_layouts[curr_index].addWidget(self.build_param_range_element("", "", ""))

    def build_param_range_element(self, curr_range_end, curr_range_start, curr_substr):
        param_widget = QWidget()
        param_widget.setFixedHeight(100)
        param_widget.setStyleSheet("border-radius: 10px; background-color: " + color.LIGHT_GRAY + ";")
        param_layout = QVBoxLayout()
        # param_layout.setAlignment(Qt.AlignCenter)
        # type
        type_layout = QHBoxLayout()
        type_combo_box = CustomComboBox()
        type_combo_box.addItem("any")
        type_combo_box.addItem("signs")
        type_combo_box.addItem("numbers")
        type_combo_box.addItem("letters")
        type_combo_box.addItem("alphanumerics")
        type_layout.addWidget(type_combo_box)
        type_layout.addWidget(AtMenuButton(
            height=20,
            minimum_width=30,
            maximum_width=30,
            font_size=10,
            border_radius=5,
            text="X",
            btn_color=color.LIGHT_REMOVE_BUTTON,
            do_when_clicked=lambda: self.remove_and_update_view(param_widget)
        ))
        param_layout.addLayout(type_layout)
        # content
        # for type: ANY
        content_text_edit = QLineEdit()
        styleSheet = "border-radius: 5px; background-color: white; padding: 5px;font-family: Arial; font-size: 14px;"
        content_text_edit.setStyleSheet(styleSheet)
        content_text_edit.setText(curr_substr)
        content_text_edit.setAlignment(Qt.AlignCenter)
        param_layout.addWidget(content_text_edit)
        # quantity
        quantity_layout = QHBoxLayout()
        start_quantity_text_edit = QLineEdit()
        start_quantity_text_edit.setStyleSheet(styleSheet)
        start_quantity_text_edit.setAlignment(Qt.AlignCenter)
        start_quantity_text_edit.setText(curr_range_start)
        quantity_layout.addWidget(start_quantity_text_edit)
        label = QLabel("to")
        label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px;")
        quantity_layout.addWidget(label)
        end_quantity_text_edit = QLineEdit()
        end_quantity_text_edit.setStyleSheet(styleSheet)
        end_quantity_text_edit.setAlignment(Qt.AlignCenter)
        end_quantity_text_edit.setText(curr_range_end)
        quantity_layout.addWidget(end_quantity_text_edit)
        param_layout.addLayout(quantity_layout)
        param_widget.setLayout(param_layout)
        return param_widget

    def remove_and_update_view(self, widget_to_remove):
        widget_to_remove.deleteLater()

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
