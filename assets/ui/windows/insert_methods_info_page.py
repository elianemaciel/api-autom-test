import os
import re

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, \
    QScrollArea, QLineEdit, QMessageBox

from assets.components import Method
from assets.ui.util import style, color
from assets.ui.widgets.combo_box import CustomComboBox
from assets.ui.widgets.dialog.set_method_params_dialog import MethodParamsDialog
from assets.ui.widgets.dialog.validation_error_dialog import ValidationErrorDialog
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.widgets.method_choice import MethodChoice
from assets.ui.widgets.method_crud import MethodCrud
from assets.ui.windows.bottom_buttons_for_add_extra_data import BottomButtonsForAddExtraData
from model.DataTypes import DATA_TYPES


def get_methods_from_test_cases(test_cases):
    methods = []
    for test_case in test_cases:
        if isinstance(test_case, Method):
            methods.append(test_case)
        else:
            #method = Method(name=test_case.method_info, class_name=test_case.className)
            method = Method(name=test_case.method, class_name=test_case.className)
            if test_case is not None and test_case.parameters is not None:
                for param in test_case.parameters:
                    method.add_param_by_arg(param)
            methods.append(method)
    return methods


def verify_save_and_show_list_page(new_method, do_to_show_next_page, do_to_go_back):
    # TODO: verify
    validation_result, field = validate_method(new_method)
    if not validation_result:
        error_message = "Invalid mandatory field: " + field + ". Please correct it before saving"
        ValidationErrorDialog(error_message).exec_()
        return
    if InsertMethodsInfoWidget.methods.count(new_method) > 0:
        index = InsertMethodsInfoWidget.methods.index(new_method)
        InsertMethodsInfoWidget.methods[index] = new_method
    else:
        InsertMethodsInfoWidget.methods.append(new_method)

    InsertMethodsInfoWidget.show_add_extra_data(InsertMethodsInfoWidget.methods, do_to_show_next_page, do_to_go_back)


def do_to_remove_method_item(method, do_to_show_next_page, do_to_go_back):
    try:
        InsertMethodsInfoWidget.methods.remove(method)
    except:
        pass
    InsertMethodsInfoWidget.show_add_extra_data(InsertMethodsInfoWidget.methods, do_to_show_next_page, do_to_go_back)


def validate_methods_and_show_error():
    valid_result = validate_current_methods()
    if valid_result is None:
        return True

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle("Validation Error")
    msg_box.setText("The method \"" + valid_result.name + "\" has empty mandatory (*) fields. Please fix it before continue")
    msg_box.exec()


def validate_valid_string(value):
    pattern = r'^[a-zA-Z_$][a-zA-Z\d_$]*$'
    return bool(re.match(pattern, value))


def validate_method(method):
    if not validate_valid_string(method.class_name):
        return False, "Class Name"
    if not validate_valid_string(method.name):
        return False, "Method Name"
    if method.output_type == '':
        return False, "Output Type"
    if len(method.params) == 0:
        return False, "Parameters"
    for param in method.params:
        if not validate_valid_string(param.name):
            return False, "Missing parameter name"
        if param.type_name == '':
            return False, "Return type of '" + param.name + "'"
    return True, ''


def validate_current_methods():
    methods = InsertMethodsInfoWidget.methods
    for method in methods:
        validation_result, _ = validate_method(method)
        if not validation_result:
            return method
    return None


class InsertMethodsInfoWidget:
    BASIC_CONTENT_INDEX = 0
    SUCCESS_ON_CONVERTING_CONTENT_INDEX = -1
    ADD_EXTRA_DATA_CONTENT_INDEX = -1
    CREATE_OR_EDIT_METHOD_CONTENT_INDEX = -1

    position = None
    instance = None
    visible_content = 0
    basic_content = None
    success_on_converting_content = None
    methods_choice = []
    methods_crud = []
    methods = []
    content = None
    parametersLayout = None

    @staticmethod
    def get_or_start(do_to_go_back, position=None, visible_content=0):

        # InsertMethodsInfoWidget._setup_basic_content()
        InsertMethodsInfoWidget.content = QStackedWidget()

        InsertMethodsInfoWidget.visible_content = visible_content
        if InsertMethodsInfoWidget.position is None and position is None:
            raise ValueError(
                "InsertMethodsInfo not started yet. position has value 'None'. Please start the page first")
        if InsertMethodsInfoWidget.position is not None:
            return InsertMethodsInfoWidget.instance
        InsertMethodsInfoWidget.position = position
        InsertMethodsInfoWidget.instance = InsertMethodsInfoWidget._setup_basic_content(lambda: None, do_to_go_back)
        InsertMethodsInfoWidget.methods_choice = []
        InsertMethodsInfoWidget.methods_crud = []
        return InsertMethodsInfoWidget.instance

    @staticmethod
    def _setup_basic_content(do_to_show_next_page, do_to_go_back):
        InsertMethodsInfoWidget.content.addWidget(InsertMethodsInfoWidget.get_basic_content())
        content_widget = InsertMethodsInfoWidget.success_content_widget(
            InsertMethodsInfoWidget.methods,
            do_to_show_next_page,
            do_to_go_back
        )
        InsertMethodsInfoWidget.content.addWidget(content_widget)
        InsertMethodsInfoWidget.SUCCESS_ON_CONVERTING_CONTENT_INDEX = InsertMethodsInfoWidget.content.indexOf(
            content_widget)
        InsertMethodsInfoWidget.content.setCurrentIndex(InsertMethodsInfoWidget.BASIC_CONTENT_INDEX)
        # InsertMethodsInfoWidget.get_basic_content()
        return InsertMethodsInfoWidget.content

    @staticmethod
    def get_basic_content():
        widget = QWidget()
        content_layout = QVBoxLayout()
        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)
        # Set application logo
        logo = QLabel()
        pixmap = QPixmap(os.path.join(os.getcwd(), 'ui/images/automtest-logo.png'))
        scaled_pixmap = pixmap.scaledToHeight(64)
        logo.setPixmap(scaled_pixmap)
        logo.resize(scaled_pixmap.width(), scaled_pixmap.height())
        logo.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(logo)
        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)
        # Set main content
        program_description = QLabel()
        program_description.setText("Content for Insert Methods Info page")
        program_description.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        program_description.setWordWrap(True)
        content_layout.addWidget(program_description)
        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)
        widget.setLayout(content_layout)
        return widget

    @staticmethod
    def show_add_extra_data(test_cases, do_to_show_next_page, do_to_go_back):
        InsertMethodsInfoWidget.methods = get_methods_from_test_cases(test_cases)
        # if the content already exists, remove to add it again
        if InsertMethodsInfoWidget.ADD_EXTRA_DATA_CONTENT_INDEX != -1:
            extra_data_widget = InsertMethodsInfoWidget.content.widget(
                InsertMethodsInfoWidget.ADD_EXTRA_DATA_CONTENT_INDEX)
            InsertMethodsInfoWidget.content.removeWidget(extra_data_widget)
        # initialize the content
        widget = InsertMethodsInfoWidget.add_extra_data_content_widget(InsertMethodsInfoWidget.methods,
                                                                       do_to_show_next_page, do_to_go_back)
        InsertMethodsInfoWidget.content.addWidget(widget)
        InsertMethodsInfoWidget.ADD_EXTRA_DATA_CONTENT_INDEX = InsertMethodsInfoWidget.content.indexOf(widget)
        # set as active content
        InsertMethodsInfoWidget.content.setCurrentIndex(InsertMethodsInfoWidget.ADD_EXTRA_DATA_CONTENT_INDEX)

    @staticmethod
    def show_converting_success(methods, do_to_show_next_page, do_to_go_back):
        # if the content already exists, remove to add it again
        if InsertMethodsInfoWidget.SUCCESS_ON_CONVERTING_CONTENT_INDEX != -1:
            converting_success_widget = InsertMethodsInfoWidget.content.widget(
                InsertMethodsInfoWidget.SUCCESS_ON_CONVERTING_CONTENT_INDEX)
            InsertMethodsInfoWidget.content.removeWidget(converting_success_widget)
        # initialize the content
        widget = InsertMethodsInfoWidget.success_content_widget(methods, do_to_show_next_page, do_to_go_back)
        InsertMethodsInfoWidget.content.addWidget(widget)
        InsertMethodsInfoWidget.SUCCESS_ON_CONVERTING_CONTENT_INDEX = InsertMethodsInfoWidget.content.indexOf(widget)
        # set as active content
        InsertMethodsInfoWidget.content.setCurrentIndex(InsertMethodsInfoWidget.SUCCESS_ON_CONVERTING_CONTENT_INDEX)

    @staticmethod
    def show_create_or_edit_method(do_to_show_next_page, do_to_go_back, method=None):
        # if the content already exists, remove to add it again
        if InsertMethodsInfoWidget.CREATE_OR_EDIT_METHOD_CONTENT_INDEX != -1:
            widget = InsertMethodsInfoWidget.content.widget(
                InsertMethodsInfoWidget.CREATE_OR_EDIT_METHOD_CONTENT_INDEX)
            InsertMethodsInfoWidget.content.removeWidget(widget)
        widget = InsertMethodsInfoWidget.create_or_edit_method_content_widget(do_to_show_next_page, do_to_go_back, method)
        InsertMethodsInfoWidget.content.addWidget(widget)
        InsertMethodsInfoWidget.CREATE_OR_EDIT_METHOD_CONTENT_INDEX = InsertMethodsInfoWidget.content.indexOf(widget)
        # set as active content
        InsertMethodsInfoWidget.content.setCurrentIndex(InsertMethodsInfoWidget.CREATE_OR_EDIT_METHOD_CONTENT_INDEX)

    @staticmethod
    def create_or_edit_method_content_widget(do_to_show_next_page, do_to_go_back, method=None):
        widget = QWidget()
        content_layout = QVBoxLayout()
        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)
        # Set header
        header = QLabel("Edit method:" if method is not None else "Create method:")
        header.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        header.setWordWrap(True)
        content_layout.addWidget(header)

        # Set spacing
        spacing = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        # Stylesheets for future use
        label_stylesheet = "padding:10px; font-size: 16px; font-weight: bold;"
        text_edit_stylesheet = "QLineEdit {border-radius: 10px; background-color: white}"

        # Package name-----------------------------------------------------------------------------
        pkg_name = QHBoxLayout()
        label = QLabel("Package name:")
        label.setStyleSheet(label_stylesheet)
        label.setStyleSheet(label_stylesheet)
        pkg_name.addWidget(label)
        pkg_name.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        pkg_name_text_edit = QLineEdit()
        pkg_name_text_edit.setStyleSheet(text_edit_stylesheet)
        pkg_name_text_edit.setText(method.package_name if method is not None else "")
        pkg_name_text_edit.setFixedHeight(40)
        pkg_name_text_edit.setFixedWidth(500)
        pkg_name.addWidget(pkg_name_text_edit)
        content_layout.addLayout(pkg_name)

        # Class name-----------------------------------------------------------------------------
        class_name = QHBoxLayout()
        label = QLabel("Class name*:")
        label.setStyleSheet(label_stylesheet)
        class_name.addWidget(label)
        class_name.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        class_name_text_edit = QLineEdit()
        class_name_text_edit.setStyleSheet(text_edit_stylesheet)
        class_name_text_edit.setText(method.class_name if method is not None else "")
        class_name_text_edit.setFixedHeight(40)
        class_name_text_edit.setFixedWidth(500)
        class_name.addWidget(class_name_text_edit)
        content_layout.addLayout(class_name)

        # Method name-----------------------------------------------------------------------------
        method_name = QHBoxLayout()
        label = QLabel("Method name*:")
        label.setStyleSheet(label_stylesheet)
        method_name.addWidget(label)
        method_name.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        method_name_text_edit = QLineEdit()
        method_name_text_edit.setStyleSheet(text_edit_stylesheet)
        method_name_text_edit.setText(method.name if method is not None else "")
        method_name_text_edit.setFixedWidth(500)
        method_name_text_edit.setFixedHeight(40)
        method_name.addWidget(method_name_text_edit)
        content_layout.addLayout(method_name)

        # Params-----------------------------------------------------------------------------
        #To be used below (but reference needed in this section)
        return_type_combo_box = CustomComboBox()
        #-----------------
        params = QHBoxLayout()

        label = QLabel("parameters*:")
        label.setStyleSheet(label_stylesheet)
        params.addWidget(label)
        params.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        scroll = QScrollArea()
        scroll.setObjectName("scroll-area")
        scroll.setFixedHeight(117)
        scroll.setFixedWidth(420)
        params.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollContent.setFixedHeight(100)
        scrollLayout = QHBoxLayout(scrollContent)
        scroll.setWidget(scrollContent)
        scroll.setStyleSheet("border: none;")
        for param in (method.params if method is not None else []):
            param_widget = QWidget()
            param_widget.setFixedHeight(70)
            param_widget.setMaximumWidth(170)
            param_widget.setStyleSheet("border-radius: 10px; background-color: white;")

            param_layout = QVBoxLayout()
            param_layout.setAlignment(Qt.AlignCenter)

            # name
            label = QLabel(param.name)
            label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px; font-weight: 600;")
            label.setAlignment(Qt.AlignCenter)
            param_layout.addWidget(label)

            # type
            label = QLabel(param.type_name)
            label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px; color: gray;")
            label.setAlignment(Qt.AlignCenter)
            param_layout.addWidget(label)

            param_widget.setLayout(param_layout)
            scrollLayout.addWidget(param_widget)

        # Set spacing
        spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
        params.addItem(spacing)
        if method is None:
            method = Method()
        edit_button_layout = QVBoxLayout()
        edit_button_layout.addItem(QSpacerItem(15, 15, QSizePolicy.Fixed, QSizePolicy.Fixed))

        edit_button_layout.addWidget(AtMenuButton(
            text="Fill\nin\ndata",  # todo: if all required fields are set, otherwise "edit data"
            minimum_width=70,
            maximum_width=70,
            height=70,
            do_when_clicked=lambda: InsertMethodsInfoWidget.show_dialog_and_update_with_result(
                Method.build_from(
                    other_method=method,
                    name=method_name_text_edit.text(),
                    class_name=class_name_text_edit.text(),
                    package_name=pkg_name_text_edit.text(),
                    output_type=return_type_combo_box.currentText()
                ),
                do_to_show_next_page,
                do_to_go_back
            )
        ))
        edit_button_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        params.addLayout(edit_button_layout)
        InsertMethodsInfoWidget.parametersLayout = params

        content_layout.addLayout(params)

        # Return type-----------------------------------------------------------------------------
        method_name = QHBoxLayout()
        label = QLabel("Return type*:")
        label.setStyleSheet(label_stylesheet)
        method_name.addWidget(label)
        method_name.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        index = 0
        for i in range(0, len(DATA_TYPES)):
            return_type_combo_box.addItem(DATA_TYPES[i])
            if method is not None and method.output_type == DATA_TYPES[i]:
                index = i
        return_type_combo_box.setCurrentIndex(index)

        return_type_combo_box.setFixedWidth(500)
        return_type_combo_box.setFixedHeight(40)
        method_name.addWidget(return_type_combo_box)
        content_layout.addLayout(method_name)

        # Set spacing----------------------------------------------------------------------------
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        # Bottom bar-----------------------------------------------------------------------------
        bottom_button_bar_layout = QHBoxLayout()
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="List all methods",
                minimum_width=170,
                do_when_clicked=lambda: InsertMethodsInfoWidget.show_add_extra_data(
                    InsertMethodsInfoWidget.methods, do_to_show_next_page, do_to_go_back),
                btn_color=color.BOTTOM_NAVIGATION_LIST_ALL
            )
        )
        bottom_button_bar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Go Back",
                minimum_width=100,
                do_when_clicked=lambda: InsertMethodsInfoWidget.show_add_extra_data(
                    InsertMethodsInfoWidget.methods, do_to_show_next_page, do_to_go_back),
                btn_color=color.BOTTOM_NAVIGATION_BACKWARD
            )
        )
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Save",
                minimum_width=100,
                do_when_clicked=lambda: (
                    verify_save_and_show_list_page(
                        Method(name=method_name_text_edit.text(),
                               class_name=class_name_text_edit.text(),
                               package_name=pkg_name_text_edit.text(),
                               output_type=return_type_combo_box.currentText(),
                               identifier=method.identifier if method is not None else None,
                               params=method.params if (method is not None and method.params is not None) else []
                               ),
                        do_to_show_next_page,
                        do_to_go_back)
                ),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)

        content_layout.addLayout(bottom_button_bar_layout)
        # content_layout.addLayout(
        #     InsertMethodsInfoWidget.setup_create_or_edit_method_content_bottom_buttons(do_to_show_next_page))

        widget.setLayout(content_layout)
        return widget


    @staticmethod
    def show_dialog_and_update_with_result(method, do_to_show_next_page, do_to_go_back):
        dialog = MethodParamsDialog(method.params, method.name)
        dialog.exec_()
        if dialog.should_update_parent_param_list():
            method.params = dialog.get_updated_list()
            print(method.params)
            if InsertMethodsInfoWidget.methods.count(method) > 0:
                index = InsertMethodsInfoWidget.methods.index(method)
                InsertMethodsInfoWidget.methods[index] = method
            else:
                InsertMethodsInfoWidget.methods.append(method)

            InsertMethodsInfoWidget.show_create_or_edit_method(
                do_to_show_next_page,
                do_to_go_back,
                method
            )

    @staticmethod
    def add_extra_data_content_widget(methods, do_to_show_next_page, do_to_go_back):
        widget = QWidget()
        content_layout = QVBoxLayout()
        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)
        # Set header
        header = QLabel("Insert extra data for each method:" if len(methods) > 0 else "Insert methods for "
                                                                                      "the tests that are going to be "
                                                                                      "created use:")
        header.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        header.setWordWrap(True)
        content_layout.addWidget(header)

        # Set spacing
        spacing = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        scroll = QScrollArea()
        content_layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scroll.setWidget(scrollContent)
        scroll.setStyleSheet("border: none;")

        # add item into the scrollable-list
        for method in methods:
            scrollLayout.addLayout(InsertMethodsInfoWidget.get_crud_method_item(method, do_to_show_next_page, do_to_go_back))

        # add a button at the end of scrollable list
        scrollLayout.addWidget(AtMenuButton(
            text="Add a New Method",
            height=40,
            btn_color=color.ADD_NEW_METHOD_BUTTON,
            do_when_clicked=lambda: InsertMethodsInfoWidget.show_create_or_edit_method(do_to_show_next_page, do_to_go_back)
        ))

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        # Set spacing
        spacing = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        # Bottom bar
        # content_layout.addLayout(InsertMethodsInfoWidget.setup_add_extra_data_content_bottom_buttons())
        content_layout.addLayout(BottomButtonsForAddExtraData(
            lambda: do_to_show_next_page() if validate_methods_and_show_error() else None,
            lambda: InsertMethodsInfoWidget.show_converting_success(
                methods,
                do_to_show_next_page,
                do_to_go_back)
        ))
        widget.setLayout(content_layout)
        return widget

    @staticmethod
    def success_content_widget(methods, do_to_show_next_page, do_to_go_back):
        widget = QWidget()
        content_layout = QVBoxLayout()
        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)
        # Set header
        header = QLabel("The User Story was successfully converted!")
        header.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        header.setWordWrap(True)
        content_layout.addWidget(header)
        suggestions = QLabel(str(len(methods)) + " methods were generated. Please, select the ones relevant "
                                                 "to your application:")
        suggestions.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        suggestions.setWordWrap(True)
        content_layout.addWidget(suggestions)

        # Set spacing
        spacing = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        scroll = QScrollArea()
        content_layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scroll.setWidget(scrollContent)
        scroll.setStyleSheet("border: none;")

        # add item na lista
        for method in methods:
            scrollLayout.addLayout(InsertMethodsInfoWidget.get_method_item(method))

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        # Set spacing
        spacing = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        # Bottom bar
        content_layout.addLayout(InsertMethodsInfoWidget.setup_success_content_bottom_buttons(
            do_to_show_next_page, do_to_go_back))

        widget.setLayout(content_layout)
        return widget

    @staticmethod
    def get_selected_methods():
        selected = []
        for method in InsertMethodsInfoWidget.methods_choice:
            if method.is_checkbox_selected():
                selected.append(method.get_method_info())
        return selected

    @staticmethod
    def get_method_item(method):
        method_choice = MethodChoice(method)
        InsertMethodsInfoWidget.methods_choice.append(method_choice)
        return method_choice

    @staticmethod
    def get_crud_method_item(method, do_to_show_next_page, do_to_go_back):
        method_crud = MethodCrud(
            method,
            do_when_edit_is_clicked=lambda: InsertMethodsInfoWidget.show_create_or_edit_method(do_to_show_next_page,
                                                                                               do_to_go_back,
                                                                                               method),
            do_when_remove_is_clicked=lambda: do_to_remove_method_item(method, do_to_show_next_page, do_to_go_back)
            # TODO: remover e atualizar lista de métodos. do_when_remove_is_clicked= InsertMethodsInfoWidget.
        )
        InsertMethodsInfoWidget.methods_crud.append(method_crud)
        return method_crud

    @staticmethod
    def setup_success_content_bottom_buttons(do_to_show_next_page, do_to_go_back):
        # Bottom button bar
        bottom_button_bar_layout = QHBoxLayout()
        spacing = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(spacing)
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Go Back",
                # height=30,
                minimum_width=100,
                do_when_clicked=do_to_go_back,
                btn_color=color.BOTTOM_NAVIGATION_BACKWARD
            )
        )
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Continue With\nSelected Methods",
                # height=30,
                minimum_width=170,
                do_when_clicked=lambda: (
                    InsertMethodsInfoWidget.show_add_extra_data(
                        InsertMethodsInfoWidget.get_selected_methods(),
                        do_to_show_next_page,
                        do_to_go_back
                    ),
                    # self.close() TODO: voltar esta linha à ativa
                ),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)
        return bottom_button_bar_layout
