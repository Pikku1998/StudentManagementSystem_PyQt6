from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, \
    QComboBox, QPushButton, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(405, 400)
        self.setWindowTitle("Student Management System")

        # Define Menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add actions to each menu item
        add_student_action = QAction(QIcon('icons/add.png'), 'Add Student', self)
        add_student_action.triggered.connect(self.insert_student)
        file_menu_item.addAction(add_student_action)
        search_student_action = QAction(QIcon('icons/search.png'), 'Search', self)
        search_student_action.triggered.connect(self.search_student)
        file_menu_item.addAction(search_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(4)
        self.student_table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile no.'))
        self.student_table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.student_table)
        self.load_table()

        # Create a toolbar and add toolbar elements
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Create a status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Detect a cell click
        self.student_table.cellClicked.connect(self.cell_selected)

    def cell_selected(self):
        edit_button = QPushButton('Edit')
        edit_button.clicked.connect(self.edit_student)

        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(self.delete_student)

        # Prevent duplicate buttons
        children = self.status_bar.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def load_table(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM STUDENTS')
        self.student_table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.student_table.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.student_table.setItem(row_number, column_number, QTableWidgetItem(str(cell_data)))
        connection.close()

    @staticmethod
    def insert_student():
        dialog = InsertDialog()
        dialog.exec()

    @staticmethod
    def search_student():
        dialog = SearchDialog()
        dialog.exec()

    @staticmethod
    def edit_student():
        dialog = EditDialog()
        dialog.exec()

    @staticmethod
    def delete_student():
        dialog = DeleteDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        self.setWindowTitle('Enter Student Data')

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        self.course_enrolled = QComboBox()
        courses = ['Computer Science', 'Data Science', 'Artificial Intelligence', 'Cyber Security', 'Mathematics']
        self.course_enrolled.addItems(courses)
        layout.addWidget(self.course_enrolled)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText('Mobile Number')
        layout.addWidget(self.mobile)

        button = QPushButton('Add this student')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_enrolled.currentText()
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?,?,?)', (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        management_system.load_table()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(100)
        self.setFixedWidth(200)
        self.setWindowTitle('Search Student')

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Enter student name')
        layout.addWidget(self.student_name)

        button = QPushButton('Search')
        layout.addWidget(button)
        button.clicked.connect(self.search)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        items = management_system.student_table.findItems(name, Qt.MatchFlag.MatchFixedString)

        for item in items:
            management_system.student_table.item(item.row(), 1).setSelected(True)


class EditDialog(QDialog):
    pass


class DeleteDialog(QDialog):
    pass


app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
sys.exit(app.exec())
