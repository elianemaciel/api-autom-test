from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QWidget, QSpacerItem, QSizePolicy, \
    QLineEdit

from assets.ui.util import color
from assets.ui.widgets.combo_box import CustomComboBox
from assets.ui.widgets.menu_button import AtMenuButton


def run_after_combo_box_index_change(content_text_edit, index):
    content_text_edit.setEnabled(index == 0)
    if index != 0:
        content_text_edit.setText("")
        content_text_edit.setStyleSheet(get_line_edit_stylesheet("gray"))
    else:
        content_text_edit.setStyleSheet(get_line_edit_stylesheet("white"))


class StringRangeLayout(QVBoxLayout):

    def __init__(self, range_value, is_return=False):
        super(StringRangeLayout, self).__init__()

        if is_return:
            label = QLabel("Below, design the pattern of the returning String")
            label.setStyleSheet("font-size: 14px;")
        else:
            label = QLabel("Building String pattern for the parameter <b>" + range_value.param.name + "</b>:")
            label.setStyleSheet("font-size: 14px;")
        self.addWidget(label)
        param_def_layout = QHBoxLayout()
        self.addLayout(param_def_layout)

        horizontal_scroll = QScrollArea()
        horizontal_scroll.setFixedHeight(170)
        horizontal_scroll.setWidgetResizable(True)
        horizontal_scroll_content = QWidget(horizontal_scroll)
        horizontal_scroll_content.setFixedHeight(153)
        self.horizontal_scroll_layout = QHBoxLayout(horizontal_scroll_content)
        horizontal_scroll.setWidget(horizontal_scroll_content)
        horizontal_scroll.setStyleSheet("border: none;")

        param_widget = QWidget()
        param_widget.setFixedHeight(133)
        param_widget.setStyleSheet("border-radius: 10px; background-color: " + color.LIGHT_GRAY + ";")

        param_label_layout = QVBoxLayout()

        label = QLabel("Type:")
        label.setStyleSheet("font-family: Arial; font-size: 14px;")
        param_label_layout.addWidget(label)

        label = QLabel("Content:")
        label.setStyleSheet("font-family: Arial; font-size: 14px;")
        param_label_layout.addWidget(label)

        label = QLabel("Quantity:")
        label.setStyleSheet("font-family: Arial; font-size: 14px;")
        param_label_layout.addWidget(label)

        label = QLabel("Move/Remove:")
        label.setStyleSheet("font-family: Arial; font-size: 14px;")
        param_label_layout.addWidget(label)

        param_widget.setLayout(param_label_layout)
        param_label_wrapper_layout = QVBoxLayout()
        param_label_wrapper_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed))
        param_label_wrapper_layout.addWidget(param_widget)
        param_label_wrapper_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        param_def_layout.addLayout(param_label_wrapper_layout)

        param_def_layout.addWidget(horizontal_scroll)

        for i in range(0, range_value.amount_of_elements()):
            curr_substr, curr_range = range_value.get_range_by_index(i)
            curr_range_start = curr_range.split("~")[0]
            curr_range_end = curr_range.split("~")[1]

            element = self.build_param_range_element(curr_range_end, curr_range_start, curr_substr)
            self.horizontal_scroll_layout.addWidget(element)

        self.horizontal_scroll_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        param_label_wrapper_layout = QVBoxLayout()
        param_label_wrapper_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed))
        param_label_wrapper_layout.addWidget(AtMenuButton(
            text="Add\nmore",
            height=133,
            minimum_width=70,
            font_size=10,
            btn_color=color.ADD_NEW_METHOD_BUTTON,
            do_when_clicked=lambda: self.add_more_on_click()
        ))
        param_label_wrapper_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        param_def_layout.addLayout(param_label_wrapper_layout)

    def get_horizontal_scroll_layout(self):
        return self.horizontal_scroll_layout

    def add_more_on_click(self):
        index = self.horizontal_scroll_layout.count() - 1
        self.horizontal_scroll_layout.insertWidget(index, self.build_param_range_element("", "", ""))

    def get_range_data(self):
        range_content_builder = ""
        range_quantity_builder = ""
        try:

            for j in range(0, self.horizontal_scroll_layout.count()):

                item = self.horizontal_scroll_layout.itemAt(j)
                if isinstance(item, QSpacerItem) or isinstance(item.widget(), QLabel):
                    continue
                type_combo_selected = item.widget().layout().itemAt(0).itemAt(0).widget().currentText()
                content_text = item.widget().layout().itemAt(1).widget().text()
                start_value = item.widget().layout().itemAt(2).layout().itemAt(0).widget().text()
                end_value = item.widget().layout().itemAt(2).layout().itemAt(2).widget().text()

                if type_combo_selected == "any":
                    range_content_builder += "[" + content_text + "]"
                else:
                    range_content_builder += "[" + type_combo_selected + "]"
                range_quantity_builder += "[" + start_value + "~" + end_value + "]"

        except Exception as e:
            print("An internal error occurred when getting data range from StringRangeLayout", e)

        print("get_range_data: " + range_content_builder + " - " + range_quantity_builder)
        return range_content_builder, range_quantity_builder

    def build_param_range_element(self, curr_range_end, curr_range_start, curr_substr):
        param_widget = QWidget()
        param_widget.setFixedHeight(133)
        param_widget.setStyleSheet("border-radius: 10px; background-color: " + color.LIGHT_GRAY + ";")
        param_layout = QVBoxLayout()

        content_text_edit = QLineEdit()

        # type
        if curr_substr == "sign":
            combo_index = 1
        elif curr_substr == "number":
            combo_index = 2
        elif curr_substr == "letter":
            combo_index = 3
        elif curr_substr == "alphanumeric":
            combo_index = 4
        else:
            combo_index = 0
        type_layout = QHBoxLayout()
        type_combo_box = CustomComboBox(do_after_set_index=lambda i: run_after_combo_box_index_change(content_text_edit, i))
        type_combo_box.setObjectName("type_combo_box")
        type_combo_box.addItem("any")
        type_combo_box.addItem("sign")
        type_combo_box.addItem("number")
        type_combo_box.addItem("letter")
        type_combo_box.addItem("alphanumeric")
        type_combo_box.setCurrentIndex(combo_index)
        type_layout.addWidget(type_combo_box)
        type_layout.addWidget(AtMenuButton(
            height=20,
            minimum_width=30,
            maximum_width=30,
            font_size=10,
            border_radius=5,
            text="?",
            btn_color=color.HELP_BUTTON,
            do_when_clicked=lambda: remove_and_update_view(param_widget)
        ))
        param_layout.addLayout(type_layout)
        # content
        content_text_edit.setObjectName("content_text_edit")
        content_text_edit.setText(curr_substr if combo_index == 0 else "")
        content_text_edit.setAlignment(Qt.AlignCenter)
        param_layout.addWidget(content_text_edit)
        # quantity
        quantity_layout = QHBoxLayout()
        start_quantity_text_edit = QLineEdit()
        start_quantity_text_edit.setObjectName("start_quantity_text_edit")
        start_quantity_text_edit.setStyleSheet(get_line_edit_stylesheet("white"))
        start_quantity_text_edit.setAlignment(Qt.AlignCenter)
        start_quantity_text_edit.setText(curr_range_start)
        quantity_layout.addWidget(start_quantity_text_edit)
        label = QLabel("to")
        label.setStyleSheet("padding:2px; font-family: Arial; font-size: 14px;")
        quantity_layout.addWidget(label)
        end_quantity_text_edit = QLineEdit()
        end_quantity_text_edit.setObjectName("end_quantity_text_edit")
        end_quantity_text_edit.setStyleSheet(get_line_edit_stylesheet("white"))
        end_quantity_text_edit.setAlignment(Qt.AlignCenter)
        end_quantity_text_edit.setText(curr_range_end)
        quantity_layout.addWidget(end_quantity_text_edit)
        param_layout.addLayout(quantity_layout)

        bottom_items_layout = QHBoxLayout()
        param_layout.addLayout(bottom_items_layout)

        bottom_items_layout.addWidget(AtMenuButton(
            height=30,
            minimum_width=30,
            maximum_width=30,
            font_size=10,
            border_radius=5,
            text="<",
            btn_color=color.EDIT_BUTTON,
            do_when_clicked=lambda: self.move_widget(param_widget, "left")
        ))
        bottom_items_layout.addWidget(AtMenuButton(
            height=30,
            minimum_width=70,
            # maximum_width=30,
            font_size=10,
            border_radius=5,
            text="Remover",
            btn_color=color.REMOVE_BUTTON,
            do_when_clicked=lambda: remove_and_update_view(param_widget)
        ))
        bottom_items_layout.addWidget(AtMenuButton(
            height=30,
            minimum_width=30,
            maximum_width=30,
            font_size=10,
            border_radius=5,
            text=">",
            btn_color=color.EDIT_BUTTON,
            do_when_clicked=lambda: self.move_widget(param_widget, "right")
        ))

        param_widget.setLayout(param_layout)
        return param_widget

    def move_widget(self, param_widget, direction):
        index = self.horizontal_scroll_layout.indexOf(param_widget)
        if direction == "left" and index - 1 >= 0:
            index -= 1
        if direction == "right" and index + 1 < (self.horizontal_scroll_layout.count() - 1):
            index += 1
        self.horizontal_scroll_layout.insertWidget(index, param_widget)


def remove_and_update_view(widget_to_remove):
    widget_to_remove.deleteLater()


def get_line_edit_stylesheet(color):
    return "border-radius: 5px; background-color: " + color + "; padding: 5px;font-family: Arial; font-size: 14px;"
