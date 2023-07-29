from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QLabel, QHBoxLayout
import os

from assets.ui.util import style, color
from assets.ui.widgets.menu_button import AtMenuButton


class SpecifyEquivClassesWidget:
    position = None
    instance = None

    @staticmethod
    def get_or_start(position=None):
        if SpecifyEquivClassesWidget.position is None and position is None:
            raise ValueError(
                "InsertMethodsInfo not started yet. position has value 'None'. Please start the page first")
        if SpecifyEquivClassesWidget.position is not None:
            return SpecifyEquivClassesWidget.instance
        SpecifyEquivClassesWidget.position = position
        SpecifyEquivClassesWidget.instance = SpecifyEquivClassesWidget._setup()
        return SpecifyEquivClassesWidget.instance

    @staticmethod
    def _setup():
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
                do_when_clicked=show_next_content(),
                btn_color=color.BOTTOM_NAVIGATION_FORWARD
            )
        )
        content_layout.addLayout(bottom_layout)

        about_page.setLayout(content_layout)
        return about_page


def show_next_content():
    # TODO: implement
    pass
