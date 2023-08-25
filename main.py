from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3


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
        self.student_table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.student_table)
        self.load_table()

    def load_table(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM STUDENTS')
        for row_number, row_data in enumerate(result):
            self.student_table.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.student_table.setItem(row_number, column_number, QTableWidgetItem(str(cell_data)))
        connection.close()


app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
sys.exit(app.exec())
