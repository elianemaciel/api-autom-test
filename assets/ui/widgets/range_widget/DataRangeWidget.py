from abc import abstractmethod

from PySide6.QtWidgets import QWidget


class DataRangeWidget(QWidget):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_data_as_param_range(self):
        print("ERROR: get_data_as_param_range not implemented")

    @abstractmethod
    def validate_fields(self):
        print('ERROR: validate_fields not implemented')

