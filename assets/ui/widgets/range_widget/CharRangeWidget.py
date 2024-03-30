import re

from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout

from assets.components import Parameter, ParamRange
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget


class CharRangeWidget(DataRangeWidget):

    def __init__(self, param_range, is_return_range=True):
        super().__init__()

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        self.param_range = param_range

        line_edit_stylesheet = "QLineEdit {border-radius: 10px; background-color: white}"
        label_stylesheet = "font-size: 14px;"

        if param_range is not None and not is_return_range:
            label = QLabel("Set the char values for parameter <b>" + param_range.param.name + "</b>")
            label.setStyleSheet("font-size: 14px;")
            layout.addWidget(label)

        label = QLabel("List the possible chars output (comma separated):")
        label.setStyleSheet(label_stylesheet)
        horizontal_layout.addWidget(label)
        self.char_line_edit = QLineEdit()
        self.char_line_edit.setStyleSheet(line_edit_stylesheet)
        self.char_line_edit.setFixedHeight(40)
        self.char_line_edit.setText(param_range.v1 if param_range else "")
        horizontal_layout.addWidget(self.char_line_edit)

        layout.addLayout(horizontal_layout)
        self.setLayout(layout)

    def get_data_as_param_range(self):
        value = self.char_line_edit.text()
        if self.param_range is not None:
            self.param_range.v1 = value
            return self.param_range
        return ParamRange(Parameter('saida_esperada', 'char'), value)

    def validate_fields(self):
        char_line = self.char_line_edit.text()
        if not re.match(r'^[A-Za-z,]+$', char_line):
            msg = 'Invalid characters definition: "' + char_line + '"'
            return False, msg

        return True, ''
