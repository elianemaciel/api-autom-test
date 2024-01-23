import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QHBoxLayout, QSpacerItem, QSizePolicy


class RadioButton(QWidget):
    def __init__(self, option1, option2):
        super().__init__()

        self.init_ui(option1, option2)

    def init_ui(self, option1, option2):
        # Create a layout
        layout = QHBoxLayout()

        # Create radio buttons
        self.radio_button1 = QRadioButton(option1)
        self.radio_button2 = QRadioButton(option2)

        # Connect radio buttons to a slot (optional)
        self.radio_button1.clicked.connect(self.on_radio_button_clicked)
        self.radio_button2.clicked.connect(self.on_radio_button_clicked)

        # Add radio buttons to the layout
        layout.addWidget(self.radio_button1)
        layout.addWidget(self.radio_button2)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))


        # Set layout for the main window
        self.setLayout(layout)

        self.radio_button1.setChecked(True)

        # self.setWindowTitle('RadioButton Example')
        # self.show()

    def get_selected(self):
        if self.radio_button1.isChecked():
            return self.radio_button1.text()
        return self.radio_button2.text()

    def on_radio_button_clicked(self):
        sender = self.sender()
        print(f'RadioButton "{sender.text()}" clicked.')

