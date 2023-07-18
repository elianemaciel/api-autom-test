from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, \
    QCheckBox, QScrollArea
import os

from assets.ui.util import style, color
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.widgets.method_choice import MethodChoice
from assets.ui.widgets.method_crud import MethodCrud


class InsertMethodsInfoWidget:
    BASIC_CONTENT_INDEX = 0
    SUCCESS_ON_CONVERTING_CONTENT_INDEX = -1
    ADD_EXTRA_DATA_CONTENT_INDEX = -1

    position = None
    instance = None
    visible_content = 0
    basic_content = None
    success_on_converting_content = None
    methods_choice = []
    methods_crud = []
    content = None

    @staticmethod
    def get_or_start(position=None, visible_content=0):

        # InsertMethodsInfoWidget._setup_basic_content()
        InsertMethodsInfoWidget.content = QStackedWidget()

        InsertMethodsInfoWidget.visible_content = visible_content
        if InsertMethodsInfoWidget.position is None and position is None:
            raise ValueError(
                "InsertMethodsInfo not started yet. position has value 'None'. Please start the page first")
        if InsertMethodsInfoWidget.position is not None:
            return InsertMethodsInfoWidget.instance
        InsertMethodsInfoWidget.position = position
        InsertMethodsInfoWidget.instance = InsertMethodsInfoWidget._setup_basic_content()
        InsertMethodsInfoWidget.methods_choice = []
        InsertMethodsInfoWidget.methods_crud = []
        return InsertMethodsInfoWidget.instance

    # @staticmethod
    # def set_page_visible():
    #     if InsertMethodsInfoWidget.visible_content == 0:

    @staticmethod
    def _setup_basic_content():
        InsertMethodsInfoWidget.content.addWidget(InsertMethodsInfoWidget.get_basic_content())
        content_widget = InsertMethodsInfoWidget.success_content_widget([])
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
    def show_add_extra_data(methods):
        # if the content already exists, remove to add it again
        if InsertMethodsInfoWidget.ADD_EXTRA_DATA_CONTENT_INDEX != -1:
            extra_data_widget = InsertMethodsInfoWidget.content.widget(
                InsertMethodsInfoWidget.ADD_EXTRA_DATA_CONTENT_INDEX)
            InsertMethodsInfoWidget.content.removeWidget(extra_data_widget)
        # initialize the content
        widget = InsertMethodsInfoWidget.add_extra_data_content_widget(methods)
        InsertMethodsInfoWidget.content.addWidget(widget)
        InsertMethodsInfoWidget.ADD_EXTRA_DATA_CONTENT_INDEX = InsertMethodsInfoWidget.content.indexOf(widget)
        # set as active content
        InsertMethodsInfoWidget.content.setCurrentIndex(InsertMethodsInfoWidget.ADD_EXTRA_DATA_CONTENT_INDEX)

    @staticmethod
    def show_converting_success(methods):
        # if the content already exists, remove to add it again
        if InsertMethodsInfoWidget.SUCCESS_ON_CONVERTING_CONTENT_INDEX != -1:
            converting_success_widget = InsertMethodsInfoWidget.content.widget(
                InsertMethodsInfoWidget.SUCCESS_ON_CONVERTING_CONTENT_INDEX)
            InsertMethodsInfoWidget.content.removeWidget(converting_success_widget)
        # initialize the content
        widget = InsertMethodsInfoWidget.success_content_widget(methods)
        InsertMethodsInfoWidget.content.addWidget(widget)
        InsertMethodsInfoWidget.SUCCESS_ON_CONVERTING_CONTENT_INDEX = InsertMethodsInfoWidget.content.indexOf(widget)
        # set as active content
        InsertMethodsInfoWidget.content.setCurrentIndex(InsertMethodsInfoWidget.SUCCESS_ON_CONVERTING_CONTENT_INDEX)

    @staticmethod
    def add_extra_data_content_widget(methods):
        widget = QWidget()
        content_layout = QVBoxLayout()
        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)
        # Set header
        header = QLabel("Insert extra data for each method:")
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
            scrollLayout.addLayout(InsertMethodsInfoWidget.get_crud_method_item(method))

        # add a button at the end of scrollable list
        scrollLayout.addWidget(AtMenuButton(
            text="Add a New Method",
            height=40,
            btn_color=color.ADD_NEW_METHOD_BUTTON
        ))

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        # Set spacing
        spacing = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        # Bottom bar
        content_layout.addLayout(InsertMethodsInfoWidget.setup_add_extra_data_content_bottom_buttons())

        widget.setLayout(content_layout)
        return widget

    @staticmethod
    def success_content_widget(methods):
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
        content_layout.addLayout(InsertMethodsInfoWidget.setup_success_content_bottom_buttons())

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
    def get_crud_method_item(method):
        method_crud = MethodCrud(method)
        InsertMethodsInfoWidget.methods_crud.append(method_crud)
        return method_crud

    @staticmethod
    def setup_add_extra_data_content_bottom_buttons():
        # Bottom button bar
        bottom_button_bar_layout = QHBoxLayout()
        spacing = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(spacing)
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Go Back",
                # height=30,
                minimum_width=100,#TODO: implementar botão voltar
                do_when_clicked=lambda: print("Voltando para onde estávamos antes"),
                btn_color=color.BOTTOM_NAVIGATION_BACKWARD
            )
        )
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Continue",
                # height=30,
                minimum_width=170,
                do_when_clicked=lambda: (
                    # InsertMethodsInfoWidget.show_add_extra_data(InsertMethodsInfoWidget.get_selected_methods()),
                    # TODO: carregar próxima página
                ),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)
        return bottom_button_bar_layout

    @staticmethod
    def setup_success_content_bottom_buttons():
        # Bottom button bar
        bottom_button_bar_layout = QHBoxLayout()
        spacing = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(spacing)
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Go Back",
                # height=30,
                minimum_width=100,
                do_when_clicked=lambda: print("Voltando para onde estávamos antes"),
                btn_color=color.BOTTOM_NAVIGATION_BACKWARD
            )
        )
        bottom_button_bar_layout.addWidget(
            AtMenuButton(
                text="Continue With\nSelected Methods",
                # height=30,
                minimum_width=170,
                do_when_clicked=lambda: (
                    InsertMethodsInfoWidget.show_add_extra_data(InsertMethodsInfoWidget.get_selected_methods()),
                    # self.close() TODO: voltar esta linha à ativa
                ),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        end_spacing = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
        bottom_button_bar_layout.addItem(end_spacing)
        return bottom_button_bar_layout
