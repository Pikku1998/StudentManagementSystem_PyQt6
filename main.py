from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, \
    QComboBox, QPushButton, QToolBar, QStatusBar, QGridLayout, QLabel, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


class DatabaseConnection:
    def __init__(self, database_file='database.db'):
        self.database = database_file

    def connect(self):
        connection = sqlite3.connect(self.database)
        return connection


def remove_statusbar_widgets():
    children = management_system.status_bar.findChildren(QPushButton)
    if children:
        for child in children:
            management_system.status_bar.removeWidget(child)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(405, 400)
        self.setWindowTitle("Student Management System")
        self.setWindowIcon(QIcon('icons/main.png'))

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

        about_action = QAction(QIcon('icons/about.png'), 'About', self)
        about_action.triggered.connect(self.about_app)
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

    @staticmethod
    def about_app():
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        self.setWindowIcon(QIcon('icons/about.png'))
        about_text = """
        Hai, 
        This app is developed by Prakash R while taking 'Python Mega Course'.
        Feel free to clone, edit the code if required.
        
        Happy Learning.
        """
        self.setText(about_text)


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        self.setWindowTitle('Enter Student Data')
        self.setWindowIcon(QIcon('icons/add.png'))

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

        button = QPushButton('Add student')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_enrolled.currentText()
        mobile = self.mobile.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?,?,?)', (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        management_system.load_table()

        self.close()

        success_message = QMessageBox()
        success_message.setWindowIcon(QIcon('icons/add.png'))
        success_message.setWindowTitle('Student Added')
        success_message.setText('The student record was added to the database.')
        success_message.exec()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(100)
        self.setFixedWidth(200)
        self.setWindowTitle('Search Student')
        self.setWindowIcon(QIcon('icons/search.png'))

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

        if items:
            for item in items:
                management_system.student_table.item(item.row(), 1).setSelected(True)
            self.close()
        else:
            message = QMessageBox()
            message.setWindowIcon(QIcon('icons/search.png'))
            message.setWindowTitle('Error')
            message.setText('No Student found.')
            message.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        self.setWindowTitle('Update Student Data')
        self.setWindowIcon(QIcon('icons/update.png'))

        layout = QVBoxLayout()

        # Get row number of the selected cell
        index = management_system.student_table.currentRow()
        # Get id, name, course, mobile from selected row
        self.student_id = management_system.student_table.item(index, 0).text()
        student_name = management_system.student_table.item(index, 1).text()
        course_enrolled = management_system.student_table.item(index, 2).text()
        mobile = management_system.student_table.item(index, 3).text()

        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        self.course_enrolled = QComboBox()
        courses = ['Computer Science', 'Data Science', 'Artificial Intelligence', 'Cyber Security', 'Mathematics']
        self.course_enrolled.addItems(courses)
        self.course_enrolled.setCurrentText(course_enrolled)
        layout.addWidget(self.course_enrolled)

        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText('Mobile Number')
        layout.addWidget(self.mobile)

        button = QPushButton('Update student data')
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        name = self.student_name.text()
        course = self.course_enrolled.currentText()
        mobile = self.mobile.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?',
                       (name, course, mobile, self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        management_system.load_table()

        self.close()

        # Remove buttons from status bar after updating.
        remove_statusbar_widgets()

        success_message = QMessageBox()
        success_message.setWindowIcon(QIcon('icons/update.png'))
        success_message.setWindowTitle('Record Updated')
        success_message.setText('The selected student record was updated successfully..')
        success_message.exec()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Confirmation')
        self.setWindowIcon(QIcon('icons/delete.png'))

        layout = QGridLayout()

        yes = QPushButton('Yes')
        no = QPushButton('No')

        confirmation_text = QLabel("Delete this record?")
        layout.addWidget(confirmation_text, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0, 1, 1)
        layout.addWidget(no, 1, 1, 1, 1)

        yes.clicked.connect(self.delete_record)
        no.clicked.connect(self.close)

        self.setLayout(layout)

    def delete_record(self):
        # Get row number of the selected cell
        index = management_system.student_table.currentRow()
        # Get id, name, course, mobile from selected row
        student_id = management_system.student_table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM students where id = ?', (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        management_system.load_table()
        self.close()

        # Remove buttons from status bar after deleting.
        remove_statusbar_widgets()

        success_message = QMessageBox()
        success_message.setWindowTitle('Deleted')
        success_message.setWindowIcon(QIcon('icons/delete.png'))
        success_message.setText('The student record was deleted successfully...')
        success_message.exec()


app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
sys.exit(app.exec())
