from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, \
    QMessageBox

from assets.ui.layouts.StringRangeLayout import StringRangeLayout
from assets.ui.util import color
from assets.ui.widgets.dialog.validation_error_dialog import ValidationErrorDialog
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.widgets.range_widget.BooleanRangeWidget import BooleanRangeWidget
from assets.ui.widgets.range_widget.CharRangeWidget import CharRangeWidget
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget
from assets.ui.widgets.range_widget.DateRangeWidget import DateRangeWidget
from assets.ui.widgets.range_widget.NumericRangeWidget import NumericRangeWidget


class EquivalenceClassParamsDialog(QDialog):
    def __init__(self, param_ranges, equiv_class_name, parent=None):
        super().__init__(parent)

        self.range_items = []

        self.setFixedWidth(800)
        self.setFixedHeight(500)
        self.current_param_range_list = param_ranges
        self.equiv_class_name = equiv_class_name
        self.parent = parent

        self.setStyleSheet("background-color: " + color.BACKGROUND + ";")
        self.setWindowTitle("Set parameter ranges for equivalence class")
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
            param_widget = QWidget()
            # param_widget.setFixedHeight(133)
            param_widget.setStyleSheet("border-radius: 10px; background-color: " + color.VERY_LIGHT_GRAY + ";")
            param_widget_layout = QVBoxLayout()
            param_widget.setLayout(param_widget_layout)
            vertical_scroll_layout.addWidget(param_widget)

            if param_range.param.type_name == "String":
                string_range_layout = StringRangeLayout(param_range)
                self.range_items.append(string_range_layout)
                param_widget_layout.addLayout(string_range_layout)

            elif param_range.param.type_name == "boolean":
                widget = BooleanRangeWidget(param_range, False)
                self.range_items.append(widget)
                param_widget_layout.addWidget(widget)

            elif param_range.param.type_name == "Date":
                widget = DateRangeWidget(param_range, False)
                self.range_items.append(widget)
                param_widget_layout.addWidget(widget)

            elif param_range.param.type_name == "char":
                widget = CharRangeWidget(param_range, False)
                self.range_items.append(widget)
                param_widget_layout.addWidget(widget)

            elif param_range.param.type_name == "int" \
                    or param_range.param.type_name == "float" \
                    or param_range.param.type_name == "double":
                widget = NumericRangeWidget(param_range, param_range.param.type_name, False)
                self.range_items.append(widget)
                param_widget_layout.addWidget(widget)

            else:
                print("Error: impossible to determine the type for parameter " + str(param_range.param))

        vertical_scroll_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
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
                do_when_clicked=lambda: self.validate_and_save(),
                btn_color=color.POPUP_BOTTOM_BUTTON_OK
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)
        self.layout.addLayout(bottom_button_bar_layout)

    def validate_and_save(self):
        for item in self.range_items:
            validation_result, error_message = item.validate_fields()
            if not validation_result:
                print('Falha ao validar campos: ' + error_message)
                ValidationErrorDialog(error_message).exec_()
                return
        self.update_current_param_range_list()
        self.close()

    def update_current_param_range_list(self):
        # TODO: verify data before saving

        for i in range(0, len(self.range_items)):

            item = self.range_items[i]
            if isinstance(item, DataRangeWidget):
                param_range = item.get_data_as_param_range()
                self.current_param_range_list[i] = param_range
            else:
                content, quantity = item.get_range_data()
                self.current_param_range_list[i].v1 = content
                self.current_param_range_list[i].v2 = quantity
