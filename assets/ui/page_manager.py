from assets.ui.windows.insert_methods_info_page import InsertMethodsInfoWidget, get_methods_from_test_cases
from assets.ui.windows.specify_equiv_classes_page import SpecifyEquivClassesWidget


class PageManager:
    main_ui = None
    instance = None

    def __init__(self, main_ui):
        PageManager.main_ui = main_ui
        PageManager.instance = self

    @staticmethod
    def show_page(position, id_button):
        PageManager.instance.set_logo_visibility(True)
        PageManager.main_ui.all_pages.setCurrentIndex(position)
        for btn in PageManager.instance.main_ui.menu_buttons:
            btn.toggle_active(btn.id == id_button)

    @staticmethod
    def show_specify_equiv_classes_start_page(methods):
        num_rows = len(methods)
        num_cols = 2
        SpecifyEquivClassesWidget.methods = [[0] * num_cols for _ in range(num_rows)]
        for i in range(0, len(methods)):
            SpecifyEquivClassesWidget.methods[i][0] = methods[i]
        print("métodos:")
        print(methods)
        print()
        PageManager.instance.show_page(SpecifyEquivClassesWidget.position, "EQUIV_CLASSES")

    @staticmethod
    def show_specify_equiv_classes_create_equiv_class_page():
        PageManager.instance.show_page(SpecifyEquivClassesWidget.position, "EQUIV_CLASSES")
        SpecifyEquivClassesWidget.show_create_equiv_class_content()

    @staticmethod
    def show_insert_methods_info():
        PageManager.instance.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")

    @staticmethod
    def show_insert_methods_info_success(test_cases):
        PageManager.instance.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")
        InsertMethodsInfoWidget.methods = get_methods_from_test_cases(test_cases)
        InsertMethodsInfoWidget.show_converting_success(
            test_cases,
            lambda: PageManager.show_specify_equiv_classes_start_page(InsertMethodsInfoWidget.methods)
        )

    @staticmethod
    def show_create_or_edit_method(method=None):
        PageManager.instance.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")
        InsertMethodsInfoWidget.show_create_or_edit_method(
            lambda: PageManager.show_specify_equiv_classes_start_page()
        )

    @staticmethod
    def show_insert_methods_info_add_extra_data(test_cases):
        PageManager.instance.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")
        InsertMethodsInfoWidget.methods = get_methods_from_test_cases(test_cases)
        InsertMethodsInfoWidget.show_add_extra_data(
            test_cases,#TODO: estão atualizados?
            lambda: PageManager.show_specify_equiv_classes_start_page(InsertMethodsInfoWidget.methods)
        )

    @staticmethod
    def set_logo_visibility(is_visible):
        PageManager.instance.main_ui.logo.setVisible(is_visible)
