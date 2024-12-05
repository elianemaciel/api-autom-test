import re
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QSizePolicy, QSpacerItem
from PySide6.QtGui import QValidator, QIntValidator

from assets.components import Parameter, ParamRange
from assets.ui.widgets.range_widget.DataRangeWidget import DataRangeWidget


class DateValidator(QValidator):

    def __init__(self, parent=None):
        super().__init__(parent)

    def validate(self, input_text, pos):
        regex = r'^(0[1-9]|[12][0-9]|3[01])[/\\-](0[1-9]|1[0-2])[/\\-]\d{4}$'
        if re.match(regex, input_text):
            return QValidator.Acceptable
        else:
            return QValidator.Invalid


class DateRangeWidget(DataRangeWidget):

    def __init__(self, param_range, is_return_range=True):
        super().__init__()

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        self.param_range = param_range

        label_stylesheet = "padding:10px; font-size: 14px;"
        edit_stylesheet = "border-radius: 5px; background-color: white; padding: 5px; font-family: Arial; font-size: 14px;"
        date_edit_stylesheet = "border-radius: 5px; background-color: white; padding: 5px; font-family: Arial; font-size: 14px; text-align: center;"

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

        self.from_day_line_edit = QLineEdit()
        self.from_month_line_edit = QLineEdit()
        self.from_year_line_edit = QLineEdit()

        self.from_day_line_edit.setFixedWidth(30)
        self.from_month_line_edit.setFixedWidth(30)
        self.from_year_line_edit.setFixedWidth(50)

        self.from_day_line_edit.setMaxLength(2)
        self.from_month_line_edit.setMaxLength(2)
        self.from_year_line_edit.setMaxLength(4)

        self.from_day_line_edit.setStyleSheet(date_edit_stylesheet)
        self.from_month_line_edit.setStyleSheet(date_edit_stylesheet)
        self.from_year_line_edit.setStyleSheet(date_edit_stylesheet)

        self.from_day_line_edit.setValidator(QIntValidator())
        self.from_month_line_edit.setValidator(QIntValidator())
        self.from_year_line_edit.setValidator(QIntValidator())

        if param_range and param_range.v1:
            from_text = param_range.v1
            day, month, year = from_text.split('/')
            self.from_day_line_edit.setText(day)
            self.from_month_line_edit.setText(month)
            self.from_year_line_edit.setText(year)

        from_date_layout = QHBoxLayout()
        from_date_layout.addWidget(self.from_day_line_edit)
        from_date_layout.addWidget(buildDateSeparator())
        from_date_layout.addWidget(self.from_month_line_edit)
        from_date_layout.addWidget(buildDateSeparator())
        from_date_layout.addWidget(self.from_year_line_edit)

        horizontal_layout.addLayout(from_date_layout)
        horizontal_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        label = QLabel("to")
        label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px; font-weight: bold;")
        horizontal_layout.addWidget(label)

        self.to_day_line_edit = QLineEdit()
        self.to_month_line_edit = QLineEdit()
        self.to_year_line_edit = QLineEdit()

        self.to_day_line_edit.setFixedWidth(30)
        self.to_month_line_edit.setFixedWidth(30)
        self.to_year_line_edit.setFixedWidth(50)

        self.to_day_line_edit.setMaxLength(2)
        self.to_month_line_edit.setMaxLength(2)
        self.to_year_line_edit.setMaxLength(4)

        self.to_day_line_edit.setStyleSheet(date_edit_stylesheet)
        self.to_month_line_edit.setStyleSheet(date_edit_stylesheet)
        self.to_year_line_edit.setStyleSheet(date_edit_stylesheet)

        self.to_day_line_edit.setValidator(QIntValidator())
        self.to_month_line_edit.setValidator(QIntValidator())
        self.to_year_line_edit.setValidator(QIntValidator())

        if param_range and param_range.v2:
            to_text = param_range.v2
            day, month, year = to_text.split('/')
            self.to_day_line_edit.setText(day)
            self.to_month_line_edit.setText(month)
            self.to_year_line_edit.setText(year)

        to_date_layout = QHBoxLayout()
        to_date_layout.addWidget(self.to_day_line_edit)
        to_date_layout.addWidget(buildDateSeparator())
        to_date_layout.addWidget(self.to_month_line_edit)
        to_date_layout.addWidget(buildDateSeparator())
        to_date_layout.addWidget(self.to_year_line_edit)
        horizontal_layout.addLayout(to_date_layout)

        layout.addLayout(horizontal_layout)
        self.setLayout(layout)

    def get_data_as_param_range(self):
        value_from = self.from_day_line_edit.text() \
                     + '/' + self.from_month_line_edit.text() \
                     + '/' + self.from_year_line_edit.text()
        value_to = self.to_day_line_edit.text() \
                   + '/' + self.to_month_line_edit.text() \
                   + '/' + self.to_year_line_edit.text()
        if self.param_range is not None:
            self.param_range.v1 = value_from
            self.param_range.v2 = value_to
            return self.param_range
        return ParamRange(Parameter('saida_esperada', 'Date'), value_from, value_to)

    def validate_fields(self):

        day_from = self.from_day_line_edit.text()
        month_from = self.from_month_line_edit.text()
        year_from = self.from_year_line_edit.text()

        value_from = day_from + '/' + month_from + '/' + year_from

        is_valid = is_valid_date(year_from, month_from, day_from)

        if not is_valid:
            msg = 'Invalid date provided: ' + value_from
            return False, msg

        day_to = self.to_day_line_edit.text()
        month_to = self.to_month_line_edit.text()
        year_to = self.to_year_line_edit.text()

        value_to = day_to + '/' + month_to + '/' + year_to

        is_valid = is_valid_date(year_to, month_to, day_to)

        if not is_valid:
            msg = 'Invalid date provided: ' + value_to
            return False, msg

        date_from = datetime(int(year_from), int(month_from), int(day_from))
        date_to = datetime(int(year_to), int(month_to), int(day_to))

        if date_to < date_from:
            msg = 'The date "From" must be less than or equal to the date "To"'
            return False, msg

        return True, ''


def is_valid_date(year, month, day):
    if len(year) != 4:
        return False
    try:
        datetime(int(year), int(month), int(day))
        return True
    except:
        return False


def buildDateSeparator():
    slashes_stylesheet = "padding:1px; font-family: Arial; font-size: 18px; font-weight: bold;"
    label = QLabel("/")
    label.setStyleSheet(slashes_stylesheet)
    return label
