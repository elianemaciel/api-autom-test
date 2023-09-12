from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout

from assets.components import Parameter, ParamRange
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget


class DateRangeWidget(DataRangeWidget):

    def __init__(self, param_range, is_return_range=True):
        super().__init__()

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        self.param_range = param_range

        label_stylesheet = "padding:10px; font-size: 14px;"
        edit_stylesheet = "border-radius: 5px; background-color: white; padding: 5px;font-family: Arial; font-size: 14px;"

        if param_range is not None and not is_return_range:
            label = QLabel("Set the possible values for parameter <b>" + param_range.param.name + "</b>")
            label.setStyleSheet("font-size: 14px;")
            layout.addWidget(label)

        label = QLabel("Define the date range:")
        label.setStyleSheet(label_stylesheet)
        horizontal_layout.addWidget(label)

        label = QLabel("from")
        label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px; font-weight: bold;")
        horizontal_layout.addWidget(label)

        self.from_quantity_line_edit = QLineEdit()
        self.from_quantity_line_edit.setObjectName("from_quantity_line_edit")
        self.from_quantity_line_edit.setStyleSheet(edit_stylesheet)
        self.from_quantity_line_edit.setAlignment(Qt.AlignCenter)
        from_text = param_range.v1 if param_range else ""
        self.from_quantity_line_edit.setText(from_text)
        horizontal_layout.addWidget(self.from_quantity_line_edit)

        label = QLabel("to")
        label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px; font-weight: bold;")
        horizontal_layout.addWidget(label)

        self.to_quantity_line_edit = QLineEdit()
        self.to_quantity_line_edit.setObjectName("to_quantity_text_edit")
        self.to_quantity_line_edit.setStyleSheet(edit_stylesheet)
        self.to_quantity_line_edit.setAlignment(Qt.AlignCenter)
        to_text = param_range.v2 if param_range else ""
        self.to_quantity_line_edit.setText(to_text)
        horizontal_layout.addWidget(self.to_quantity_line_edit)

        layout.addLayout(horizontal_layout)
        self.setLayout(layout)

    def get_data_as_param_range(self):
        value_from = self.from_quantity_line_edit.text()
        value_to = self.to_quantity_line_edit.text()
        if self.param_range is not None:
            self.param_range.v1 = value_from
            self.param_range.v2 = value_to
            return self.param_range
        return ParamRange(Parameter('saida_esperada', 'Date'), value_from, value_to)
