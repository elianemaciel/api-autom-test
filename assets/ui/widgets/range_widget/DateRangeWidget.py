from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit

from assets.components import Parameter, ParamRange
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget


class DateRangeWidget(DataRangeWidget):

    def __init__(self, equiv_class):
        super().__init__()

        layout = QHBoxLayout()

        label_stylesheet = "padding:10px; font-size: 16px; font-weight: bold;"
        edit_stylesheet = "border-radius: 5px; background-color: white; padding: 5px;font-family: Arial; font-size: 14px;"

        label = QLabel("Define the date range:")
        label.setStyleSheet(label_stylesheet)
        layout.addWidget(label)

        label = QLabel("from")
        label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px;")
        layout.addWidget(label)

        self.from_quantity_line_edit = QLineEdit()
        self.from_quantity_line_edit.setObjectName("from_quantity_line_edit")
        self.from_quantity_line_edit.setStyleSheet(edit_stylesheet)
        self.from_quantity_line_edit.setAlignment(Qt.AlignCenter)
        from_text = equiv_class.expected_range.v1 if equiv_class and equiv_class.expected_range else ""
        self.from_quantity_line_edit.setText(from_text)
        layout.addWidget(self.from_quantity_line_edit)

        label = QLabel("to")
        label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px;")
        layout.addWidget(label)

        self.to_quantity_line_edit = QLineEdit()
        self.to_quantity_line_edit.setObjectName("to_quantity_text_edit")
        self.to_quantity_line_edit.setStyleSheet(edit_stylesheet)
        self.to_quantity_line_edit.setAlignment(Qt.AlignCenter)
        to_text = equiv_class.expected_range.v2 if equiv_class and equiv_class.expected_range else ""
        self.to_quantity_line_edit.setText(to_text)
        layout.addWidget(self.to_quantity_line_edit)

        self.setLayout(layout)

    def get_data_as_param_range(self):
        value_from = self.from_quantity_line_edit.text()
        value_to = self.to_quantity_line_edit.text()
        return ParamRange(Parameter('saida_esperada', 'Date'), value_from, value_to)
