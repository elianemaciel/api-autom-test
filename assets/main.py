## Import modules

import sys
import os

from assets.ui.windows import about_page
from qt_core import *
from ui.windows.main_window.ui_main_window import UI_MainWindow


#Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutomTest 3.0 - Gerador de Testes Unitários Automatizados")

        #Setup Main Window
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        #Clicks
        #self.ui.btn_about.clicked.connect(self.show_about_page)


        #Show the application
        self.show()

    def show_about_page(self):
        self.ui.pages.setCurrentWidget(about_page.get_about_widget())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

