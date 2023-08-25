from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(410, 400)
        self.setWindowTitle("Student Management System")

        # Define Menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add actions to each menu item
        add_student_action = QAction('Add Student', self)
        file_menu_item.addAction(add_student_action)
        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(4)
        self.student_table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile no.'))
        self.setCentralWidget(self.student_table)


app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
sys.exit(app.exec())
