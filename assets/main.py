## Import modules

import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from assets.ui.windows.main_window.ui_main_window import UI_MainWindow


#Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutomTest 3.0 - Gerador de Testes Unitários Automatizados")

        #Setup Main Window
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        path = os.path.join(os.getcwd(), 'ui/images/logo_icon.png')
        app_icon = QIcon(path)
        app.setWindowIcon(app_icon)

        #Clicks
        #self.ui.btn_about.clicked.connect(self.show_about_page)


        #Show the application
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

