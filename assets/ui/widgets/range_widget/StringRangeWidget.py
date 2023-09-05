from assets.components import ParamRange, Parameter
from assets.ui.layouts.StringRangeLayout import StringRangeLayout
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget


class StringRangeWidget(DataRangeWidget):

    def __init__(self, equiv_class):
        super().__init__()
        if equiv_class and equiv_class.expected_range:
            return_range = equiv_class.expected_range
        else:
            return_range = ParamRange(Parameter('saida_esperada', 'String'))

        self.layout = StringRangeLayout(return_range, is_return=True)
        self.setLayout(self.layout)

    def get_data_as_param_range(self):
        content, quantity = self.layout.get_range_data()
        return ParamRange(Parameter('saida_esperada', 'String'), content, quantity)
