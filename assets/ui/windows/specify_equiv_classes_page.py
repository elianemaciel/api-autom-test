from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QStackedWidget, \
    QLineEdit

from assets.ui.util import style, color
from assets.ui.widgets.combo_box import CustomComboBox
from assets.ui.widgets.dialog.set_equiv_class_params_dialog import EquivalenceClassParamsDialog
from assets.ui.widgets.menu_button import AtMenuButton


class SpecifyEquivClassesWidget:
    HELP_CONTENT_INDEX = 0
    CREATE_EQUIV_CLASS_CONTENT_INDEX = -1

    content = None
    position = None
    instance = None
    visible_content = 0

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
    def show_create_equiv_class_content():
        # if the content already exists, remove to add it again
        if SpecifyEquivClassesWidget.CREATE_EQUIV_CLASS_CONTENT_INDEX != -1:
            content_widget = SpecifyEquivClassesWidget.content.widget(
                SpecifyEquivClassesWidget.CREATE_EQUIV_CLASS_CONTENT_INDEX)
            SpecifyEquivClassesWidget.content.removeWidget(content_widget)
        # initialize the content
        widget = SpecifyEquivClassesWidget._create_equiv_class_content_widget()
        SpecifyEquivClassesWidget.content.addWidget(widget)
        SpecifyEquivClassesWidget.CREATE_EQUIV_CLASS_CONTENT_INDEX = SpecifyEquivClassesWidget.content.indexOf(widget)
        # set as active content
        SpecifyEquivClassesWidget.content.setCurrentIndex(SpecifyEquivClassesWidget.CREATE_EQUIV_CLASS_CONTENT_INDEX)
        print("definido show_create_equiv_class_content com sucesso. Index:" + str(SpecifyEquivClassesWidget.CREATE_EQUIV_CLASS_CONTENT_INDEX))

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

        # # Set application logo
        # logo = QLabel()
        # pixmap = QPixmap(os.path.join(os.getcwd(), 'ui/images/automtest-logo.png'))
        # scaled_pixmap = pixmap.scaledToHeight(64)
        # logo.setPixmap(scaled_pixmap)
        # logo.resize(scaled_pixmap.width(), scaled_pixmap.height())
        # logo.setAlignment(Qt.AlignCenter)
        # content_layout.addWidget(logo)

        # Set spacing
        # spacing = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # content_layout.addItem(spacing)

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

        # what = QLabel()
        # what.setText("""
        #
        # """)
        # what.setStyleSheet(style.EXPLANATION_APPLICATION_TEXT)
        # what.setWordWrap(True)
        # content_layout.addWidget(what)

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
                do_when_clicked=lambda: print("Voltando para onde estávamos antes"),
                btn_color=color.BOTTOM_NAVIGATION_LIST_ALL
            )
        )
        # Set spacing
        bottom_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_layout.addWidget(
            AtMenuButton(
                text="Add",
                minimum_width=220,
                do_when_clicked=lambda: SpecifyEquivClassesWidget.show_create_equiv_class_content(),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        content_layout.addLayout(bottom_layout)

        about_page.setLayout(content_layout)
        return about_page

    @staticmethod
    def _create_equiv_class_content_widget():
        about_page = QWidget()
        content_layout = QVBoxLayout()

        # Set spacing
        spacing = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
        content_layout.addItem(spacing)

        # Set header-------------------------------------------------------------------------------
        title = QLabel()
        title.setText("Choose a method and specify an equivalence class for it:")
        title.setStyleSheet(style.BASIC_APPLICATION_TEXT)
        title.setWordWrap(True)
        content_layout.addWidget(title)

        # Method Selection-----------------------------------------------------------------------------
        label_stylesheet = "padding:10px; font-size: 16px; font-weight: bold;"
        method_name_layout = QHBoxLayout()
        label = QLabel("Select the method:")
        label.setStyleSheet(label_stylesheet)
        method_name_layout.addWidget(label)
        method_name_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        combo_box = CustomComboBox()
        combo_box.addItem("hasTeacherProfile")
        combo_box.addItem("isLegalAge")
        combo_box.addItem("makeRoomReservation")
        combo_box.setFixedWidth(500)
        combo_box.setFixedHeight(40)
        method_name_layout.addWidget(combo_box)
        content_layout.addLayout(method_name_layout)

        # Equiv class name-----------------------------------------------------------------------------
        text_edit_stylesheet = "QLineEdit {border-radius: 10px; background-color: white}"
        expected_retun_layout = QHBoxLayout()
        label = QLabel("Equivalence class name:")
        label.setStyleSheet(label_stylesheet)
        expected_retun_layout.addWidget(label)
        expected_retun_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        from_text_edit = QLineEdit()
        from_text_edit.setStyleSheet(text_edit_stylesheet)
        from_text_edit.setFixedHeight(40)
        from_text_edit.setFixedWidth(400)
        expected_retun_layout.addWidget(from_text_edit)
        content_layout.addLayout(expected_retun_layout)

        # Number of test cases-----------------------------------------------------------------------------
        text_edit_stylesheet = "QLineEdit {border-radius: 10px; background-color: white}"
        expected_retun_layout = QHBoxLayout()
        label = QLabel("Number of test cases to be generated:")
        label.setStyleSheet(label_stylesheet)
        expected_retun_layout.addWidget(label)
        expected_retun_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        from_text_edit = QLineEdit()
        from_text_edit.setStyleSheet(text_edit_stylesheet)
        from_text_edit.setFixedHeight(40)
        from_text_edit.setFixedWidth(400)
        expected_retun_layout.addWidget(from_text_edit)
        content_layout.addLayout(expected_retun_layout)

        # Specify parameters button-------------------------------------------------------------------------------
        content_layout.addWidget(AtMenuButton(
            text="Specify Parameters",
            height=40,
            btn_color=color.ADD_NEW_METHOD_BUTTON,
            do_when_clicked=lambda: (EquivalenceClassParamsDialog(param_list=["Age"], equiv_class_name="valid_input").exec_())
        ))

        # Expected return values-----------------------------------------------------------------------------
        text_edit_stylesheet = "QLineEdit {border-radius: 10px; background-color: white}"
        expected_retun_layout = QHBoxLayout()

        label = QLabel("Expected returns (Integer number):")
        label.setStyleSheet(label_stylesheet)
        content_layout.addWidget(label)

        label = QLabel("From:")
        label.setStyleSheet(label_stylesheet)
        expected_retun_layout.addWidget(label)

        from_text_edit = QLineEdit()
        from_text_edit.setStyleSheet(text_edit_stylesheet)
        from_text_edit.setFixedHeight(40)
        # from_text_edit.setFixedWidth(100)
        expected_retun_layout.addWidget(from_text_edit)

        label = QLabel("To:")
        label.setStyleSheet(label_stylesheet)
        expected_retun_layout.addWidget(label)

        to_text_edit = QLineEdit()
        to_text_edit.setStyleSheet(text_edit_stylesheet)
        to_text_edit.setFixedHeight(40)
        # to_text_edit.setFixedWidth(100)
        expected_retun_layout.addWidget(to_text_edit)

        label = QLabel("Also include\n (comma separated):")
        label.setStyleSheet(label_stylesheet)
        expected_retun_layout.addWidget(label)

        also_include_text_edit = QLineEdit()
        also_include_text_edit.setStyleSheet(text_edit_stylesheet)
        also_include_text_edit.setFixedHeight(40)
        # also_include_text_edit.setFixedWidth(200)
        expected_retun_layout.addWidget(also_include_text_edit)

        content_layout.addLayout(expected_retun_layout)
        # bottom buttons--------------------------------------------------------------------------------

        # Set spacing
        content_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(
            AtMenuButton(
                text="List equivalence\n classes",
                # height=30,
                maximum_width=170,
                minimum_width=170,
                do_when_clicked=lambda: print("Voltando para onde estávamos antes"),
                btn_color=color.BOTTOM_NAVIGATION_LIST_ALL
            )
        )
        # Set spacing
        bottom_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_layout.addWidget(
            AtMenuButton(
                text="Cancel",
                minimum_width=170,
                do_when_clicked=lambda: print("go back"),
                btn_color=color.BOTTOM_NAVIGATION_BACKWARD
            )
        )
        content_layout.addLayout(bottom_layout)
        bottom_layout.addWidget(
            AtMenuButton(
                text="Add another",
                minimum_width=170,
                do_when_clicked=lambda: SpecifyEquivClassesWidget.show_create_equiv_class_content(),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        content_layout.addLayout(bottom_layout)

        about_page.setLayout(content_layout)
        return about_page


def show_next_content():
    # TODO: implement
    pass
