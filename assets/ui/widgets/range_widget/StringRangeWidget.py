from assets.components import ParamRange, Parameter
from assets.ui.layouts.StringRangeLayout import StringRangeLayout
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget


class StringRangeWidget(DataRangeWidget):

    def __init__(self, param_range=None):
        super().__init__()
        if param_range is None:
            param_range = ParamRange(Parameter('saida_esperada', 'String'))

        self.layout = StringRangeLayout(param_range, is_return=True)
        self.setLayout(self.layout)

    def get_data_as_param_range(self):
        content, quantity = self.layout.get_range_data()
        return ParamRange(Parameter('saida_esperada', 'String'), content, quantity)

    def validate_fields(self):
        return self.layout.validate_fields()
