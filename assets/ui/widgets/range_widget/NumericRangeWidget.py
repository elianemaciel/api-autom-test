from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit

from assets.components import ParamRange, Parameter
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget

NUMERIC_TYPE_INTEGER = "int"
NUMERIC_TYPE_FLOAT = "float"
NUMERIC_TYPE_DOUBLE = "double"


class NumericRangeWidget(DataRangeWidget):

    def __init__(self, numeric_type, equiv_class):
        super().__init__()

        self.also_include_text_edit = QLineEdit()
        self.to_text_edit = QLineEdit()
        self.from_text_edit = QLineEdit()
        self.numeric_type = numeric_type

        layout = self.build_numeric_range(
            equiv_class.expected_range.v1 if equiv_class else "",
            equiv_class.expected_range.v2 if equiv_class else "",
            equiv_class.expected_range.v3 if equiv_class else "",
        )

        self.setLayout(layout)

    def build_numeric_range(self, from_content, to_content, also_include_content):
        layout = QHBoxLayout()
        text_edit_stylesheet = "QLineEdit {border-radius: 10px; background-color: white}"
        label_stylesheet = "padding:10px; font-size: 16px; font-weight: bold;"
        label = QLabel("From:")
        label.setStyleSheet(label_stylesheet)
        layout.addWidget(label)
        self.from_text_edit.setStyleSheet(text_edit_stylesheet)
        self.from_text_edit.setFixedHeight(40)
        self.from_text_edit.setText(from_content)
        layout.addWidget(self.from_text_edit)
        label = QLabel("To:")
        label.setStyleSheet(label_stylesheet)
        layout.addWidget(label)
        self.to_text_edit.setStyleSheet(text_edit_stylesheet)
        self.to_text_edit.setFixedHeight(40)
        self.to_text_edit.setText(to_content)
        layout.addWidget(self.to_text_edit)
        label = QLabel("Also include\n (comma separated):")
        label.setStyleSheet(label_stylesheet)
        layout.addWidget(label)
        self.also_include_text_edit.setStyleSheet(text_edit_stylesheet)
        self.also_include_text_edit.setFixedHeight(40)
        self.also_include_text_edit.setText(also_include_content)
        layout.addWidget(self.also_include_text_edit)
        return layout

    def get_data_as_param_range(self):
        from_value = self.from_text_edit.text()
        to_value = self.to_text_edit.text()
        also_include = self.also_include_text_edit.text()
        return ParamRange(Parameter('saida_esperada', self.numeric_type), from_value, to_value, also_include)
