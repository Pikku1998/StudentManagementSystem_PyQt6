from PyQt6.QtWidgets import QMainWindow, QApplication
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")


app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
sys.exit(app.exec())
