from assets.ui.windows.insert_methods_info_page import InsertMethodsInfoWidget
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
    def show_specify_equiv_classes_start_page():
        PageManager.instance.show_page(SpecifyEquivClassesWidget.position, "EQUIV_CLASSES")

    @staticmethod
    def show_specify_equiv_classes_create_equiv_class_page():
        PageManager.instance.show_page(SpecifyEquivClassesWidget.position, "EQUIV_CLASSES")
        SpecifyEquivClassesWidget.show_create_equiv_class_content()

    @staticmethod
    def show_insert_methods_info():
        PageManager.instance.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")

    @staticmethod
    def show_insert_methods_info_success(methods):
        PageManager.instance.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")
        InsertMethodsInfoWidget.show_converting_success(
            methods,
            lambda: PageManager.show_specify_equiv_classes_start_page()
        )

    @staticmethod
    def show_create_or_edit_method(method=None):
        PageManager.instance.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")
        InsertMethodsInfoWidget.show_create_or_edit_method(
            lambda: PageManager.show_specify_equiv_classes_start_page()
        )

    @staticmethod
    def show_insert_methods_info_add_extra_data(methods):
        PageManager.instance.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")
        InsertMethodsInfoWidget.show_add_extra_data(
            methods,
            lambda: PageManager.show_specify_equiv_classes_start_page()
        )

    @staticmethod
    def set_logo_visibility(is_visible):
        PageManager.instance.main_ui.logo.setVisible(is_visible)
