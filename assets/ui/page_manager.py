import threading

from assets.ui.windows.insert_methods_info_page import InsertMethodsInfoWidget, get_methods_from_test_cases
from assets.ui.windows.specify_equiv_class.specify_equiv_classes_page import SpecifyEquivClassesWidget
import schedule
import time

from assets.ui.windows.user_story_page import InsertUserStoryWidget


class PageManager:
    main_ui = None
    instance = None

    def __init__(self, main_ui):
        PageManager.main_ui = main_ui
        PageManager.instance = self

        job_thread = threading.Thread(target=PageManager.schedule_buttons_states)
        job_thread.start()

    @staticmethod
    def show_page(position, id_button):
        for btn in PageManager.instance.main_ui.menu_buttons:
            if btn.id == id_button and not btn.is_clickable:
                return  # ignoring because it's not clickable at the current application state
        for btn in PageManager.instance.main_ui.menu_buttons:
            btn.toggle_active(btn.id == id_button)
        if InsertMethodsInfoWidget.position == position:
            PageManager.show_insert_methods_info_add_extra_data([])
        PageManager.instance.set_logo_visibility(not id_button == "ABOUT")
        PageManager.main_ui.all_pages.setCurrentIndex(position)

    @staticmethod
    def toggle_buttons_state():
        for btn in PageManager.instance.main_ui.menu_buttons:
            is_clickable = True
            if btn.id == "EQUIV_CLASSES":
                is_clickable = len(InsertMethodsInfoWidget.methods) > 0
            elif btn.id == "TESTS":
                is_clickable = SpecifyEquivClassesWidget.has_any_equiv_class()
            # print(btn.id + " > " + str(is_clickable))
            if not btn.is_clickable == is_clickable:
                btn.toggle_clickable(is_clickable)

    @staticmethod
    def schedule_buttons_states():
        schedule.every(1).second.do(PageManager.toggle_buttons_state)
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                print("Error while toggling buttons state: ", e)

    @staticmethod
    def show_specify_equiv_classes_start_page(methods):
        num_rows = len(methods)
        num_cols = 2
        SpecifyEquivClassesWidget.methods = [[0] * num_cols for _ in range(num_rows)]
        for i in range(0, len(methods)):
            SpecifyEquivClassesWidget.methods[i][0] = methods[i]
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
            lambda: PageManager.show_specify_equiv_classes_start_page(InsertMethodsInfoWidget.methods),
            lambda: PageManager.show_insert_user_story()
        )

    @staticmethod
    def show_create_or_edit_method(method=None):
        PageManager.instance.show_page(InsertMethodsInfoWidget.position, "INSERT_INFO")
        InsertMethodsInfoWidget.show_create_or_edit_method(
            lambda: PageManager.show_specify_equiv_classes_start_page()
        )

    @staticmethod
    def show_insert_methods_info_add_extra_data(test_cases):
        InsertMethodsInfoWidget.methods = get_methods_from_test_cases(test_cases)
        InsertMethodsInfoWidget.show_add_extra_data(
            test_cases,
            lambda: PageManager.show_specify_equiv_classes_start_page(InsertMethodsInfoWidget.methods)
        )

    @staticmethod
    def set_logo_visibility(is_visible):
        PageManager.instance.main_ui.logo.setVisible(is_visible)

    @staticmethod
    def show_insert_user_story():
        PageManager.instance.show_page(InsertUserStoryWidget.position, "USER_STORY")
