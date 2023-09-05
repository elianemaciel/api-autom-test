from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit

from assets.components import Parameter, ParamRange
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget


class CharRangeWidget(DataRangeWidget):

    def __init__(self, equiv_class):
        super().__init__()

        layout = QHBoxLayout()

        line_edit_stylesheet = "QLineEdit {border-radius: 10px; background-color: white}"
        label_stylesheet = "padding:10px; font-size: 16px; font-weight: bold;"

        label = QLabel("List the possible chars output\n(comma separated):")
        label.setStyleSheet(label_stylesheet)
        layout.addWidget(label)
        self.char_line_edit = QLineEdit()
        self.char_line_edit.setStyleSheet(line_edit_stylesheet)
        self.char_line_edit.setFixedHeight(40)
        self.char_line_edit.setText(equiv_class.expected_range.v1 if equiv_class and equiv_class.expected_range else "")
        layout.addWidget(self.char_line_edit)

        self.setLayout(layout)

    def get_data_as_param_range(self):
        value = self.char_line_edit.text()
        return ParamRange(Parameter('saida_esperada', 'char'), value)
