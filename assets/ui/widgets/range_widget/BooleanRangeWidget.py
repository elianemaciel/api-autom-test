from PySide6.QtWidgets import QHBoxLayout, QLabel

from assets.components import ParamRange, Parameter
from assets.ui.widgets.combo_box import CustomComboBox
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget


class BooleanRangeWidget(DataRangeWidget):

    def __init__(self, equiv_class):
        super().__init__()

        layout = QHBoxLayout()

        label_stylesheet = "padding:10px; font-size: 16px; font-weight: bold;"
        label = QLabel("Choose the possible boolean output:")
        label.setStyleSheet(label_stylesheet)
        layout.addWidget(label)

        self.bool_combo_box = CustomComboBox()
        self.bool_combo_box.addItem("true")
        self.bool_combo_box.addItem("false")
        index = 1 if equiv_class and equiv_class.expected_range and equiv_class.expected_range.v1 == 'false' else 0
        self.bool_combo_box.setCurrentIndex(index)
        layout.addWidget(self.bool_combo_box)

        self.setLayout(layout)

    def get_data_as_param_range(self):
        value = self.bool_combo_box.currentText()
        return ParamRange(Parameter('saida_esperada', 'boolean'), value)
