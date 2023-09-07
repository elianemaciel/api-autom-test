from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QStackedWidget, \
    QLineEdit, QScrollArea

from assets.components import ParamRange, TestSet, Parameter
from assets.ui.util import style, color
from assets.ui.widgets.VariableParamClickableButton import VariableParamClickableButton
from assets.ui.widgets.range_widget.BooleanRangeWidget import BooleanRangeWidget
from assets.ui.widgets.range_widget.CharRangeWidget import CharRangeWidget
from assets.ui.widgets.range_widget.DateRangeWidget import DateRangeWidget
from assets.ui.widgets.range_widget.NumericRangeWidget import NumericRangeWidget, NUMERIC_TYPE_INTEGER, \
    NUMERIC_TYPE_FLOAT, NUMERIC_TYPE_DOUBLE
from assets.ui.widgets.range_widget.StringRangeWidget import StringRangeWidget
from assets.ui.widgets.combo_box import CustomComboBox
from assets.ui.widgets.dialog.set_equiv_class_params_dialog import EquivalenceClassParamsDialog
from assets.ui.widgets.menu_button import AtMenuButton
from assets.ui.widgets.param_range_add_button import ParamRangeAddButton


def do_when_change_method_selection(index):
    SpecifyEquivClassesWidget.show_create_equiv_class_content(
        method=SpecifyEquivClassesWidget.methods[index][0],
        keep_combo_box=True)


# def remove_equiv_class(method_index, equiv_class):
def remove_equiv_class(params):
    # SpecifyEquivClassesWidget.methods[method_index][0].remove_testset(equiv_class)
    SpecifyEquivClassesWidget.methods[params[0]][0].remove_testset(params[1])
    SpecifyEquivClassesWidget.show_list_equiv_class_content()


class SpecifyEquivClassesWidget:
    HELP_CONTENT_INDEX = 0
    CREATE_EQUIV_CLASS_CONTENT_INDEX = -1
    LIST_EQUIV_CLASS_CONTENT_INDEX = -1

    content = None
    position = None
    instance = None
    methods = []
    visible_content = 0
    combo_box = None
    return_widget = None

    @staticmethod
    def get_or_start(position=None, visible_content=0):

        SpecifyEquivClassesWidget.content = QStackedWidget()
        SpecifyEquivClassesWidget.visible_content = visible_content

        if SpecifyEquivClassesWidget.position is None and position is None:
            raise ValueError(
                "InsertMethodsInfo not started yet. position has value 'None'. Please start the page first")
        if SpecifyEquivClassesWidget.position is not None:
            return SpecifyEquivClassesWidget.instance
        SpecifyEquivClassesWidget.position = position
        SpecifyEquivClassesWidget.instance = SpecifyEquivClassesWidget.show_help_content()
        return SpecifyEquivClassesWidget.instance

    @staticmethod
    def show_create_equiv_class_content(method=None, equiv_class=None, is_edit=False, keep_combo_box=False):
        # if the content already exists, remove to add it again
        if SpecifyEquivClassesWidget.CREATE_EQUIV_CLASS_CONTENT_INDEX != -1:
            content_widget = SpecifyEquivClassesWidget.content.widget(
                SpecifyEquivClassesWidget.CREATE_EQUIV_CLASS_CONTENT_INDEX)
            SpecifyEquivClassesWidget.content.removeWidget(content_widget)
        # initialize the content
        widget = SpecifyEquivClassesWidget._create_equiv_class_content_widget(method, equiv_class, is_edit, keep_combo_box)
        SpecifyEquivClassesWidget.content.addWidget(widget)
        SpecifyEquivClassesWidget.CREATE_EQUIV_CLASS_CONTENT_INDEX = SpecifyEquivClassesWidget.content.indexOf(widget)
        # set as active content
        SpecifyEquivClassesWidget.content.setCurrentIndex(SpecifyEquivClassesWidget.CREATE_EQUIV_CLASS_CONTENT_INDEX)

    @staticmethod
    def show_list_equiv_class_content():
        # if the content already exists, remove to add it again
        if SpecifyEquivClassesWidget.LIST_EQUIV_CLASS_CONTENT_INDEX != -1:
            content_widget = SpecifyEquivClassesWidget.content.widget(
                SpecifyEquivClassesWidget.LIST_EQUIV_CLASS_CONTENT_INDEX)
            SpecifyEquivClassesWidget.content.removeWidget(content_widget)
        # initialize the content
        widget = SpecifyEquivClassesWidget._list_equiv_class_content_widget()
        SpecifyEquivClassesWidget.content.addWidget(widget)
        SpecifyEquivClassesWidget.LIST_EQUIV_CLASS_CONTENT_INDEX = SpecifyEquivClassesWidget.content.indexOf(widget)
        # set as active content
        SpecifyEquivClassesWidget.content.setCurrentIndex(SpecifyEquivClassesWidget.LIST_EQUIV_CLASS_CONTENT_INDEX)
        print("definido show_list_equiv_class_content com sucesso. Index:" + str(SpecifyEquivClassesWidget.LIST_EQUIV_CLASS_CONTENT_INDEX))

    @staticmethod
    def show_help_content():
        content_widget = SpecifyEquivClassesWidget._help_content_widget()
        SpecifyEquivClassesWidget.content.addWidget(content_widget)
        SpecifyEquivClassesWidget.HELP_CONTENT_INDEX = SpecifyEquivClassesWidget.content.indexOf(
            content_widget)
        SpecifyEquivClassesWidget.content.setCurrentIndex(SpecifyEquivClassesWidget.HELP_CONTENT_INDEX)
        return SpecifyEquivClassesWidget.content

    @staticmethod
    def _help_content_widget():
        about_page = QWidget()
        content_layout = QVBoxLayout()

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        # Set main content
        title = QLabel()
        title.setText("Equivalence Classes")
        title.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        content_layout.addWidget(title)

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        an_example = QLabel()
        an_example.setText("""
            What Are:
            Here, an equivalence class is a tuple of a set of methods parameters and a set of possible return values for those parameters.
                
            Observe the following example:
            the method isMaiorDeIdade(inteiro idade), which has as responsibility check whether a person's of legal age, returns true in case the provided age is greater tha or equal to 18 years old and false otherwise. For that example,  we could define two equivalence classes: 
            1. The class of legal age people, with return value true and, in the parameters set 18 and 65.
            2. The class of minor agr people, with return value false and, as parameter set, 0, 1, 15 and 17, for
            example.
                
            With those info, it's possible to define a equivalence class.
            Now it's your your turn: insert the equivalence classes you decide relevant to each previously mapped
            method.
        """)
        an_example.setStyleSheet(style.EXPLANATION_APPLICATION_TEXT)
        an_example.setWordWrap(True)
        content_layout.addWidget(an_example)

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content_layout.addItem(spacing)

        # bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(
            AtMenuButton(
                text="List equivalence\n classes",
                # height=30,
                maximum_width=170,
                minimum_width=170,
                do_when_clicked=lambda: SpecifyEquivClassesWidget.show_list_equiv_class_content(),
                btn_color=color.BOTTOM_NAVIGATION_LIST_ALL
            )
        )
        # Set spacing
        bottom_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_layout.addWidget(
            AtMenuButton(
                text="Add",
                minimum_width=220,
                do_when_clicked=lambda: SpecifyEquivClassesWidget.show_create_equiv_class_content(None),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        content_layout.addLayout(bottom_layout)

        about_page.setLayout(content_layout)
        return about_page

    @staticmethod
    def _create_equiv_class_content_widget(method, equiv_class, is_edit, keep_combo_box):
        if method is None:
            method = SpecifyEquivClassesWidget.methods[0][0]

        page = QWidget()
        content_layout = QVBoxLayout()
        page.setLayout(content_layout)

        vertical_scroll = QScrollArea()
        vertical_scroll.setWidgetResizable(True)
        vertical_scroll_content = QWidget(vertical_scroll)
        vertical_scrollable_content_layout = QVBoxLayout(vertical_scroll_content)
        content_layout.addWidget(vertical_scroll)
        content_layout.addWidget(vertical_scroll)
        vertical_scroll.setWidget(vertical_scroll_content)
        vertical_scroll.setStyleSheet("border: none;")

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
        vertical_scrollable_content_layout.addItem(spacing)

        # Set header-------------------------------------------------------------------------------
        title = QLabel()
        title.setText("Choose a method and specify an equivalence class for it:")
        title.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        title.setWordWrap(True)
        vertical_scrollable_content_layout.addWidget(title)

        # Method Selection-----------------------------------------------------------------------------
        label_stylesheet = "padding:10px; font-size: 16px; font-weight: bold;"
        method_name_layout = QHBoxLayout()
        label = QLabel("Select the method:")
        label.setStyleSheet(label_stylesheet)
        method_name_layout.addWidget(label)
        method_name_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        if not keep_combo_box:
            SpecifyEquivClassesWidget.combo_box = CustomComboBox(lambda i: do_when_change_method_selection(i))
            for m in SpecifyEquivClassesWidget.methods:
                SpecifyEquivClassesWidget.combo_box.addItem(m[0].name)
            SpecifyEquivClassesWidget.combo_box.setCurrentIndex(SpecifyEquivClassesWidget.find_index_by_method(method))
            SpecifyEquivClassesWidget.combo_box.setFixedHeight(40)
        SpecifyEquivClassesWidget.combo_box.setEnabled(not is_edit)
        method_name_layout.addWidget(SpecifyEquivClassesWidget.combo_box)
        vertical_scrollable_content_layout.addLayout(method_name_layout)

        # Equiv class name-----------------------------------------------------------------------------
        text_edit_stylesheet = "QLineEdit {border-radius: 10px; background-color: white}"
        numeric_return_layout = QHBoxLayout()
        label = QLabel("Equivalence class name:")
        label.setStyleSheet(label_stylesheet)
        numeric_return_layout.addWidget(label)
        numeric_return_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        equiv_class_name_line_edit = QLineEdit()
        equiv_class_name_line_edit.setStyleSheet(text_edit_stylesheet)
        equiv_class_name_line_edit.setFixedHeight(40)
        equiv_class_name_line_edit.setText(equiv_class.name if equiv_class else "")
        numeric_return_layout.addWidget(equiv_class_name_line_edit)
        vertical_scrollable_content_layout.addLayout(numeric_return_layout)

        # Number of test cases-----------------------------------------------------------------------------
        text_edit_stylesheet = "QLineEdit {border-radius: 10px; background-color: white}"
        numeric_return_layout = QHBoxLayout()
        label = QLabel("Number of test cases to be generated:")
        label.setStyleSheet(label_stylesheet)
        numeric_return_layout.addWidget(label)
        numeric_return_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        num_test_cases_line_edit = QLineEdit()
        num_test_cases_line_edit.setStyleSheet(text_edit_stylesheet)
        num_test_cases_line_edit.setFixedHeight(40)
        num_test_cases_line_edit.setText(equiv_class.number_of_cases if equiv_class else "")
        numeric_return_layout.addWidget(num_test_cases_line_edit)
        vertical_scrollable_content_layout.addLayout(numeric_return_layout)

        # Specify parameters button-------------------------------------------------------------------------------
        vertical_scrollable_content_layout.addWidget(AtMenuButton(
            text="Specify Parameters",
            height=40,
            btn_color=color.ADD_NEW_METHOD_BUTTON,
            do_when_clicked=lambda: (SpecifyEquivClassesWidget.setup_and_call_param_dialog())
        ))

        # Expected return values-----------------------------------------------------------------------------

        type_label_content = "Unknown"
        SpecifyEquivClassesWidget.return_widget = NumericRangeWidget(NUMERIC_TYPE_INTEGER, equiv_class)
        if method.output_type.lower() == 'int':
            type_label_content = "Integer number"
        elif method.output_type.lower() == 'float':
            type_label_content = "Float number"
            SpecifyEquivClassesWidget.return_widget = NumericRangeWidget(NUMERIC_TYPE_FLOAT, equiv_class)
        elif method.output_type.lower() == 'double':
            type_label_content = "Double number"
            SpecifyEquivClassesWidget.return_widget = NumericRangeWidget(NUMERIC_TYPE_DOUBLE, equiv_class)
        elif method.output_type.lower() == 'string':
            type_label_content = "String"
            SpecifyEquivClassesWidget.return_widget = StringRangeWidget(equiv_class)
        elif method.output_type.lower() == 'char':
            type_label_content = "Character"
            SpecifyEquivClassesWidget.return_widget = CharRangeWidget(equiv_class)
        elif method.output_type.lower() == 'boolean':
            type_label_content = "Boolean"
            SpecifyEquivClassesWidget.return_widget = BooleanRangeWidget(equiv_class)
        elif method.output_type.lower() == 'date':
            type_label_content = "Date dd/MM/yyyy or dd-MM-yyyy"
            SpecifyEquivClassesWidget.return_widget = DateRangeWidget(equiv_class)

        label = QLabel("Expected returns (" + type_label_content + "):")
        label.setStyleSheet(label_stylesheet)
        vertical_scrollable_content_layout.addWidget(label)
        vertical_scrollable_content_layout.addWidget(SpecifyEquivClassesWidget.return_widget)

        # bottom buttons--------------------------------------------------------------------------------

        # Set spacing
        vertical_scrollable_content_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        bottom_layout = QHBoxLayout()
        # Set spacing
        bottom_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_layout.addWidget(
            AtMenuButton(
                text="Cancel",
                minimum_width=170,
                do_when_clicked=lambda: SpecifyEquivClassesWidget.show_list_equiv_class_content(),
                btn_color=color.BOTTOM_NAVIGATION_BACKWARD
            )
        )
        bottom_layout.addWidget(
            AtMenuButton(
                text="Save",
                minimum_width=170,
                do_when_clicked=lambda: SpecifyEquivClassesWidget.save_and_show_again(
                    SpecifyEquivClassesWidget.methods[SpecifyEquivClassesWidget.combo_box.currentIndex()][0],
                    SpecifyEquivClassesWidget.methods[SpecifyEquivClassesWidget.combo_box.currentIndex()][1],
                    equiv_class_name_line_edit.text(),
                    num_test_cases_line_edit.text(),
                    is_edit,
                    equiv_class
                ),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        content_layout.addLayout(bottom_layout)

        return page

    @staticmethod
    def find_index_by_method(method):
        for i in range(0, len(SpecifyEquivClassesWidget.methods)):
            if SpecifyEquivClassesWidget.methods[i][0] == method:
                return i

    @staticmethod
    def setup_and_call_param_dialog():
        curr_method_index = SpecifyEquivClassesWidget.combo_box.currentIndex()
        #TODO: é sempre para um método específico somente
        if not SpecifyEquivClassesWidget.methods[curr_method_index][1]:
            param_ranges = []
            for param in SpecifyEquivClassesWidget.methods[curr_method_index][0].params:
                param_ranges.append(ParamRange(param))
            SpecifyEquivClassesWidget.methods[curr_method_index][1] = param_ranges

        params_dialog = EquivalenceClassParamsDialog(
            SpecifyEquivClassesWidget.methods[curr_method_index][1],
            equiv_class_name="valid_input")
        params_dialog.exec_()
        SpecifyEquivClassesWidget.methods[curr_method_index][1] = params_dialog.current_param_range_list
        params_dialog.deleteLater()

    @staticmethod
    def save_and_show_again(method, equiv_class_param_ranges, equiv_class_name, num_test_cases, is_edit, equiv_class):
        #todo: verify fields and show popup error in case it's not all set

        # update methods info
        return_range = SpecifyEquivClassesWidget.return_widget.get_data_as_param_range()
        if not equiv_class:
            equiv_class = TestSet(equiv_class_name, num_test_cases, return_range)
        else:
            equiv_class.name = equiv_class_name
            equiv_class.number_of_cases = num_test_cases
            equiv_class.expected_range = return_range
        equiv_class.clear_params()
        for equiv_class_param_range in equiv_class_param_ranges:
            equiv_class.add_param_range(equiv_class_param_range)#TODO: assert data validity
        method.add_or_update_testset(equiv_class)
        # update method list
        index = SpecifyEquivClassesWidget.find_index_by_method(method)
        SpecifyEquivClassesWidget.methods[index][0] = method
        # show view to create a new equiv class
        return SpecifyEquivClassesWidget.show_list_equiv_class_content()

    @staticmethod
    def _list_equiv_class_content_widget():
        page = QWidget()
        content_layout = QVBoxLayout()

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        # Set header-------------------------------------------------------------------------------
        title = QLabel()
        title.setText("List of Equivalence Classes")
        title.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        content_layout.addWidget(title)

        # set scroll layout

        scroll = QScrollArea()
        content_layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scroll.setWidget(scrollContent)
        scroll.setStyleSheet("border: none;")

        #dentro de method temos os testsets, q são as classes de equiv que precisamos aqui. Então testamos: se
        for method in SpecifyEquivClassesWidget.methods:
            for equiv_class in method[0].testsets:
                item_widget = QWidget()
                # item_widget.setFixedHeight(70)
                item_widget.setStyleSheet("border-radius: 10px; background-color: white;")

                item_layout = QVBoxLayout()

                method_layout = QHBoxLayout()
                label = QLabel("Method:")
                label.setFixedHeight(40)
                label.setFixedWidth(170)
                label.setStyleSheet("padding:10px; font-family: Arial;  font-size: 14px; font-weight: bold;")
                method_layout.addWidget(label)
                label = QLabel(method[0].name)
                label.setFixedHeight(40)
                label.setStyleSheet("""
                    border-radius: 10px; 
                    background-color: """ + color.LIGHT_GRAY + """; 
                    padding:10px;
                    font-family: Arial; 
                    font-size: 14px;
                """)
                method_layout.addWidget(label)
                method_layout.addWidget(ParamRangeAddButton(
                    id=SpecifyEquivClassesWidget.find_index_by_method(method[0]),
                    text="Edit",
                    height=40,
                    minimum_width=100,
                    maximum_width=100,
                    btn_color=color.EDIT_BUTTON,
                    do_when_clicked=lambda i: SpecifyEquivClassesWidget.show_create_equiv_class_content(
                        SpecifyEquivClassesWidget.methods[i][0], equiv_class, True)
                ))
                item_layout.addLayout(method_layout)

                equiv_class_layout = QHBoxLayout()
                label = QLabel("Equivalence class:")
                label.setFixedHeight(40)
                label.setFixedWidth(170)
                label.setStyleSheet("padding:10px; font-family: Arial;  font-size: 14px; font-weight: bold;")
                equiv_class_layout.addWidget(label)
                label = QLabel(equiv_class.name)
                label.setFixedHeight(40)
                label.setStyleSheet("""
                    border-radius: 10px; 
                    background-color: """ + color.LIGHT_GRAY + """; 
                    padding:10px;
                    font-family: Arial; 
                    font-size: 14px;
                """)
                equiv_class_layout.addWidget(label)
                equiv_class_layout.addWidget(VariableParamClickableButton(
                    text="Remove",
                    height=40,
                    minimum_width=100,
                    maximum_width=100,
                    btn_color=color.REMOVE_BUTTON,
                    do_when_clicked=lambda params: remove_equiv_class(params),
                    do_when_clicked_params=[SpecifyEquivClassesWidget.find_index_by_method(method[0]), equiv_class]
                ))
                item_layout.addLayout(equiv_class_layout)

                item_widget.setLayout(item_layout)
                scrollLayout.addWidget(item_widget)

        scrollLayout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # bottom buttons--------------------------------------------------------------------------------

        # Set spacing
        content_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(
            AtMenuButton(
                text="Help",
                # height=30,
                maximum_width=170,
                minimum_width=170,
                do_when_clicked=lambda: SpecifyEquivClassesWidget.show_help_content(),
                btn_color=color.BOTTOM_NAVIGATION_LIST_ALL
            )
        )
        bottom_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_layout.addWidget(
            AtMenuButton(
                text="Add another",
                minimum_width=170,
                do_when_clicked=lambda: SpecifyEquivClassesWidget.show_create_equiv_class_content(),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        content_layout.addLayout(bottom_layout)

        page.setLayout(content_layout)
        return page

    @staticmethod
    def has_any_equiv_class():
        for method in SpecifyEquivClassesWidget.methods:
            if len(method[0].testsets) > 0:
                return True
        return False
