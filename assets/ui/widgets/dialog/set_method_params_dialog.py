from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, \
    QTextEdit

from assets.components import Parameter
from assets.ui.util import color
from assets.ui.widgets.combo_box import CustomComboBox
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.widgets.param_edit_item import ParamEditItem


class MethodParamsDialog(QDialog):
    def __init__(self, params, method_name, parent=None):
        super().__init__(parent)

        self.current_params_list = params

        self.setStyleSheet("background-color: " + color.BACKGROUND + ";")
        self.setWindowTitle("Warnings when converting User Story")
        self.layout = QVBoxLayout()

        message = QLabel("Define parameters for " + method_name)
        message.setStyleSheet("padding:10px; font-size: 14px;")
        message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(message)
        self.setFixedWidth(600)
        self.setFixedHeight(300)

        scroll = QScrollArea()
        self.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        # scrollContent.cl
        scrollLayout = QVBoxLayout(scrollContent)
        scroll.setWidget(scrollContent)
        scroll.setStyleSheet("border: none;")

        for param in params:
            scrollLayout.addLayout(self.build_param_item(param, scrollLayout, scrollContent, scroll))
        # list_example = []#TODO: (1) ver como fazer o botão Remove funcionar (2) salvar estado da lista antes de grandes momentos (cliques em botões)
        # list_example.remove()
        #     __delitem__(param)
        add_button = AtMenuButton(
            text="Add",
            btn_color=color.ADD_NEW_METHOD_BUTTON,
            height=30,
            do_when_clicked=lambda: (self.current_params_list.append(Parameter('', '')),
                                     self.update_list(scroll))
        )
        # scrollLayout.addWidget(add_button)
        self.layout.addWidget(add_button)

        self.setLayout(self.layout)
        self.setup_bottom_buttons(params)

    def update_list(self, scroll):
        #Save current state of params and remove current elements
        layout = scroll.widget().layout()
        while layout.count() > 0:
            item = layout.takeAt(0)
            if isinstance(item, ParamEditItem):
                for i in range(0, len(self.current_params_list)):
                    if self.current_params_list[i].identifier is item.get_param().identifier:
                        self.current_params_list[i] = item.get_param()
                        break
                print(item)
                item.layout().deleteLater()

        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scroll.setWidget(scrollContent)
        scroll.setStyleSheet("border: none;")

        for item in self.current_params_list:
            scrollLayout.addLayout(self.build_param_item(item, scrollLayout, scrollContent, scroll))

    def build_param_item(self, param, scroll_layout, scrollContent, scroll):
        print("Building param:" + param.name)
        return ParamEditItem(
            param,
            do_when_remove_is_clicked=lambda: (
                self.current_params_list.remove(param),
                self.update_list(scroll)
            )
        )

    # Function to update the list shown in the scroll layout

    def setup_bottom_buttons(self, params_updated):
        # Bottom button bar
        bottom_button_bar_layout = QHBoxLayout()
        spacing = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(spacing)
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Save",
                height=30,
                minimum_width=90,
                do_when_clicked=lambda: (
                    # PageManager.show_insert_methods_info_success(methods),
                    self.close()
                ),
                btn_color=color.POPUP_BOTTOM_BUTTON_OK
            )
        )
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Cancel",
                height=30,
                minimum_width=90,
                do_when_clicked=lambda: self.close(),
                btn_color=color.POPUP_BOTTOM_BUTTON_CANCEL
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)
        self.layout.addLayout(bottom_button_bar_layout)
