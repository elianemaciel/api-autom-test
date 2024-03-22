from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget

from assets.components import Parameter
from assets.ui.util import color
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.widgets.param_edit_item import ParamEditItem


class MethodParamsDialog(QDialog):
    def __init__(self, params, method_name, parent=None):
        super().__init__(parent)

        self.updated_parent_param_list = False
        self.current_params_list = params

        self.setStyleSheet("background-color: " + color.BACKGROUND + ";")
        self.setWindowTitle("Setting Method Params")
        self.layout = QVBoxLayout()

        message = QLabel("Define parameters for " + method_name)
        message.setStyleSheet("padding:10px; font-size: 14px;")
        message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(message)
        self.setFixedWidth(600)
        self.setFixedHeight(300)

        self.scroll = QScrollArea()
        self.layout.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        scrollContent = QWidget(self.scroll)
        # scrollContent.cl
        scrollLayout = QVBoxLayout(scrollContent)
        self.scroll.setWidget(scrollContent)
        self.scroll.setStyleSheet("border: none;")

        for param in params:
            scrollLayout.addLayout(self.build_param_item(param))
        # list_example = []#TODO: (1) ver como fazer o botão Remove funcionar (2) salvar estado da lista antes de grandes momentos (cliques em botões)
        # list_example.remove()
        #     __delitem__(param)
        add_button = AtMenuButton(
            text="Add",
            btn_color=color.ADD_NEW_METHOD_BUTTON,
            height=30,
            do_when_clicked=lambda: (self.current_params_list.append(Parameter('', '')),
                                     self.update_list())
        )
        # scrollLayout.addWidget(add_button)
        self.layout.addWidget(add_button)

        self.setLayout(self.layout)
        self.setup_bottom_buttons(params)

    def get_updated_list(self):
        self.update_list()
        return self.current_params_list

    def should_update_parent_param_list(self):
        return self.updated_parent_param_list

    def update_list(self):
        #Save current state of params and remove current elements
        layout = self.scroll.widget().layout()
        while layout.count() > 0:
            item = layout.takeAt(0)
            if isinstance(item, ParamEditItem):
                for i in range(0, len(self.current_params_list)):
                    if self.current_params_list[i].identifier is item.get_param().identifier:
                        self.current_params_list[i] = item.get_param()
                        break
                # print(item)
                item.layout().deleteLater()

        scrollContent = QWidget(self.scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        self.scroll.setWidget(scrollContent)
        self.scroll.setStyleSheet("border: none;")

        for item in self.current_params_list:
            scrollLayout.addLayout(self.build_param_item(item))

    def build_param_item(self, param):
        # print("Building param:" + param.name)
        return ParamEditItem(
            param,
            do_when_remove_is_clicked=lambda: (
                self.current_params_list.remove(param),
                self.update_list()
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
                do_when_clicked=lambda: self.upon_save(),
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

    def upon_save(self):
        self.updated_parent_param_list = True
        self.close()