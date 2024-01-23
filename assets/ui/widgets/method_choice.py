from PySide6.QtWidgets import QHBoxLayout, QCheckBox, QLabel

from assets.components import Method


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
        if isinstance(self.method_info, Method):
            parameters = ", ".join(str(item) for item in self.method_info.params) if self.method_info.params else ""
        else:
            parameters = ", ".join(str(item) for item in self.method_info.parameters) if self.method_info.parameters else ""
        item_description = QLabel(
            "<html>"
            + "<b>Class:</b> " + (self.method_info.class_name if isinstance(self.method_info, Method) else self.method_info.className)
            + "<br><b>Method:</b> " + (self.method_info.name if isinstance(self.method_info, Method) else self.method_info.method)
            + "<br><b>Parameters:</b> " + parameters
            + "<br><b>Return type:</b> " + (self.method_info.output_type if isinstance(self.method_info, Method) else "")
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

