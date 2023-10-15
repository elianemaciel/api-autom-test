from PySide6.QtWidgets import QHBoxLayout, QCheckBox, QLabel


class MethodChoice(QHBoxLayout):
    def __init__(self,
                 method,
                 is_active=True
                 ):
        super().__init__()
        self.is_active = is_active
        # checkbox
        self.item_checkbox = QCheckBox()
        self.item_checkbox.setChecked(True)
        self.item_checkbox.setObjectName("self.item_checkbox")
        self.item_checkbox.setFixedWidth(20)
        self.method_info = method
        self.addWidget(self.item_checkbox)
        # Text label with info
        parameters = ", ".join(str(item) for item in self.method_info.parameters) if self.method_info.parameters else ""
        item_description = QLabel(
            "<html>"
            + "<b>Method:</b> " + self.method_info.method
            + "<br><b>Parameters:</b> " + parameters
            + " </html>")
        item_description.setStyleSheet("""
                               QLabel {
                                   border-radius: 10px; 
                                   background-color: white; 
                                   padding:10px;
                                   font-family: Arial; 
                                   font-size: 14px;
                               }
                               """)
        item_description.setWordWrap(True)
        self.addWidget(item_description)

    def is_checkbox_selected(self):
        try:
            return self.item_checkbox.isChecked()
        except:
            return False

    def get_method_info(self):
        return self.method_info

