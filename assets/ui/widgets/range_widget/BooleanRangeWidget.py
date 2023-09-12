from PySide6.QtWidgets import QHBoxLayout, QLabel

from assets.components import ParamRange, Parameter
from assets.ui.widgets.combo_box import CustomComboBox
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget


class BooleanRangeWidget(DataRangeWidget):

    def __init__(self, param_range=None, is_return_range=True):
        super().__init__()

        layout = QHBoxLayout()
        self.param_range = param_range

        if param_range and not is_return_range:
            label = QLabel("Choose the boolean value for parameter <b>" + param_range.param.name + "</b>")
            label.setStyleSheet("font-size: 14px;")
            layout.addWidget(label)
        if is_return_range:
            label = QLabel("Choose the possible boolean output:")
            label.setStyleSheet("font-size: 14px;")
            layout.addWidget(label)

        self.bool_combo_box = CustomComboBox()
        self.bool_combo_box.addItem("true")
        self.bool_combo_box.addItem("false")
        self.bool_combo_box.setCurrentIndex(1 if param_range and param_range.v1 == "false" else 0)
        layout.addWidget(self.bool_combo_box)

        self.setLayout(layout)

    def get_data_as_param_range(self):
        value = self.bool_combo_box.currentText()
        if self.param_range is not None:
            self.param_range.v1 = value
            return self.param_range
        return ParamRange(Parameter('saida_esperada', 'boolean'), value)
