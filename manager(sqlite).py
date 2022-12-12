import os
import datetime
import time
import sys
from datetime import datetime
from datetime import timedelta
import os.path
import pprint
import sqlite3
from database_query import if_not_exists
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.SignUpButton = QtWidgets.QPushButton("Sign up")
        self.LogInButton = QtWidgets.QPushButton("Log in")
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()
        self.SignUpButton.setFixedSize(150, 25)
        self.LogInButton.setFixedSize(150, 25)
        layout.addWidget(self.SignUpButton)
        layout.addWidget(self.LogInButton)
        self.SignUpButton.clicked.connect(self.go_to_signup)
        self.LogInButton.clicked.connect(self.go_to_login)
        self.setLayout(layout)

    def go_to_login(self):
        self.LGW = LogInWindow()
        self.LGW.show()

    def go_to_signup(self):
        self.SUW = SignUpWindow()
        self.SUW.show()


class LogInWindow(QWidget):
    def __init__(self):
        super(LogInWindow, self).__init__()
        self.setWindowTitle("Log in")
        self.usernameLabel = QtWidgets.QLabel("Username")
        self.passwordLabel = QtWidgets.QLabel("Password")
        self.backButton = QtWidgets.QPushButton('Back')
        self.loginButton = QtWidgets.QPushButton('Log in')
        self.errorLabel = QtWidgets.QLabel('The email or password is incorrect.')
        self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()
        # self.backButton.clicked.connect(self.go_back)
        self.errorLabel.setStyleSheet("color : 'red'")
        self.passwordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.login_function)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        # buttonLayout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.passwordLine.setFixedSize(200, 25)
        self.usernameLine.setFixedSize(200, 25)
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameLine)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordLine)
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.loginButton)
        layout.addWidget(self.backButton)
        self.errorLabel.hide()
        self.setLayout(layout)

    # def go_back(self):
    # os.system('cls')
    # widget.setCurrentIndex(widget.currentIndex() - 1)

    def login_function(self):
        username = self.usernameLine.text()
        password = self.passwordLine.text()
        if len(username) == 0 or len(password) == 0:
            self.errorLabel.setText("Please input all fields.")
            self.errorLabel.show()
        else:
            if SignUp().user_exists(username):
                if Tasks().compare_data(username, password):
                    # self.errorLabel.setText("Successfully logged in.")
                    # self.errorLabel.setStyleSheet("color : 'green'")
                    # self.errorLabel.show()
                    # TaskManagerUI().data_receiver(username, password)
                    username_session.append(username)
                    password_session.append(password)
                    self.go_to_task_manager()
                    self.close()
                    MW.close()

                else:
                    self.errorLabel.setText("Invalid username or password")
                    self.errorLabel.show()
            else:
                self.errorLabel.setText("User not found")
                self.errorLabel.show()

    def go_to_task_manager(self):
        self.TMUI = TaskManagerUI()
        self.TMUI.show()


class SignUpWindow(QWidget):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        self.setWindowTitle('Sign up')
        self.usernameLabel = QtWidgets.QLabel("Username")
        self.passwordLabel = QtWidgets.QLabel("Password")
        self.passwordLabel2 = QtWidgets.QLabel("Confirm password")
        self.backButton = QtWidgets.QPushButton('Back')
        self.createButton = QtWidgets.QPushButton('Create user')
        self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()
        self.passwordLine2 = QtWidgets.QLineEdit()
        self.errorLabel = QtWidgets.QLabel('ERROR')
        self.errorLabel.setStyleSheet("color : 'red'")
        # self.backButton.clicked.connect(self.go_back)
        self.createButton.clicked.connect(self.create_func)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordLine.setFixedSize(200, 25)
        self.passwordLine2.setFixedSize(200, 25)
        self.usernameLine.setFixedSize(200, 25)
        layout.maximumSize()
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameLine)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordLine)
        layout.addWidget(self.passwordLabel2)
        layout.addWidget(self.passwordLine2)
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.createButton)
        layout.addWidget(self.backButton)
        self.errorLabel.hide()
        self.setLayout(layout)

    # def go_back(self):
    # widget.setCurrentIndex(widget.currentIndex() - 1)

    def create_func(self):
        username = self.usernameLine.text()
        password = self.passwordLine.text()
        password1 = self.passwordLine2.text()
        Tasks().compare_data(username, password)
        if password != password1:
            self.errorLabel.setText("Passwords are not matching")
            self.errorLabel.show()
            QtCore.QTimer.singleShot(5, SignUpWindow.close)
            LogInWindow().go_to_task_manager()
        else:
            if SignUp().user_exists(username):
                self.errorLabel.setText("User already exists")
                self.errorLabel.show()
            else:
                DataBase().database_sign_up(username, password)
                # self.errorLabel.setText('Succesfully signed up!')
                # self.errorLabel.setStyleSheet("color : 'green'")
                # self.errorLabel.show()
                self.close()
        LogInWindow().go_to_task_manager()


class TaskManagerUI(QMainWindow):
    def __init__(self):
        super(TaskManagerUI, self).__init__()
        self.setFixedSize(800, 400)
        self.setWindowTitle('Task manager')

        self.menu = QtWidgets.QMenu
        self.toolbar = QtWidgets.QToolBar()
        self.list = QtWidgets.QListWidget()

        self.addToolBar(self.toolbar)
        self.toolbar.setMovable(False)
        self.clear_button = QtWidgets.QPushButton('clear')
        self.button_action = QAction("All tasks", self)
        self.button_action.triggered.connect(self.all_tasks)
        self.button_action2 = QAction("Add task", self)
        self.button_action2.triggered.connect(self.add_task)
        self.button_action3 = QAction("Tasks status", self)
        self.button_action3.triggered.connect(self.tasks_status)
        self.button_action4 = QAction("Update status", self)
        self.button_action4.triggered.connect(self.update_status)

        self.toolbar.setStyleSheet('background-color: white;')
        self.toolbar.addAction(self.button_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.button_action2)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.button_action3)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.button_action4)

        self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()

        self.list.setStyleSheet('QListWidget::item {color:white;}')
        self.setCentralWidget(self.list)

    def clear_list(self):
        self.list.clear()

    def re_tasks(self):
        username = username_session[0]
        return DataBase().database_all_tasks(username)

    def all_tasks(self):
        for i in self.re_tasks():
            # print(str(i))
            self.list.addItem(str(i))

    def add_task(self):
        self.dialog = DialogWindow()
        self.dialog.show()

    def tasks_status(self):
        # DataBase().database_task_status(username, password, status_choice)
        pass

    def update_status(self):
        pass


# dialog window for add task func
class DialogWindow(QWidget):
    def __init__(self):
        super(DialogWindow, self).__init__()
        self.setWindowTitle('Add task')
        self.setFixedSize(400, 300)

        self.add_button = QtWidgets.QPushButton('Add')
        self.date_edit = QtWidgets.QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFixedHeight(30)
        self.date_edit.setStyleSheet('QDateEdit {color: #D3D3D3}')
        self.date_edit.setDateTime(QtCore.QDateTime.currentDateTime())

        self.user_input = QtWidgets.QLineEdit()

        self.label = QtWidgets.QLabel('Input your task')
        self.label.setStyleSheet('QLabel{font-size: 15pt}')
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.check_box = QtWidgets.QCheckBox()
        self.check_box.setText('Add steps ?')
        self.check_box.setStyleSheet('QCheckBox {color: #D3D3D3;}')
        self.check_box.stateChanged.connect(lambda: self.checked())

        self.error_label = QtWidgets.QLabel('Input integer')
        self.error_label.setStyleSheet('QLabel {color: red}')

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.user_input)
        layout.setSpacing(20)
        layout.addWidget(self.date_edit)
        layout.setSpacing(20)
        layout.addWidget(self.check_box)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.temp = self.date_edit.date()
        date.append(self.temp)

        self.add_button.clicked.connect(self.add_func)

    def checked(self):
        if self.check_box.isChecked():
            self.dialog()

    def dialog(self):
        self.ask = AskUser()
        self.ask.show()

    def add_func(self):
        self.text = self.user_input.text()
        content_session.append(self.text)
        DataBase().database_add_task()

class AskUser(QWidget):
    def __init__(self):
        super(AskUser, self).__init__()
        self.resize(300, 150)
        self.setWindowTitle('Steps')
        self.items = []
        self.item_count = 0

        label = QtWidgets.QLabel("Number of steps")
        self.accept_btn = QtWidgets.QPushButton('Accept')
        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setRange(0, 5)
        self.spinBox.valueChanged.connect(self.set_item_count)
        self.spinBox.setStyleSheet('QSpinBox {color: #D3D3D3}')
        groupBox = QtWidgets.QGroupBox("Input steps")
        groupBox.setStyleSheet('QGroupBox{color: #D3D3D3}')
        self.item_layout = QtWidgets.QVBoxLayout(groupBox)
        self.item_layout.addStretch(2)

        g_layout = QtWidgets.QGridLayout(self)
        g_layout.addWidget(label, 0, 0, 1, 2)
        g_layout.addWidget(self.spinBox, 0, 2, 1, 1)
        g_layout.addWidget(groupBox, 2, 0, 5, 3)
        g_layout.addWidget(self.accept_btn)

    def set_item_count(self, new_count: int):
        lineEdit = QtWidgets.QLineEdit
        n_items = len(self.items)
        for i in range(n_items, new_count):
            item = lineEdit(self)
            self.items.append(item)
            self.item_layout.insertWidget(n_items, item)
        for i in range(self.item_count, new_count):
            self.item_layout.itemAt(i).widget().show()
        for i in range(new_count, self.item_count):
            self.item_layout.itemAt(i).widget().hide()
        self.item_count = new_count

        if n_items > new_count:
            self.items = self.items[:-1]

        self.accept_btn.clicked.connect(self.accept_func)



    def accept_func(self):
        steps = []
        for i in self.items:
            steps.append(i.text())
        self.steps_str = ''
        for i in steps:
            self.steps_str = ', '.join([str(item) for item in steps])
        steps_session.append(self.steps_str)
        print('iz func', steps_session[0])

    """def accept_func(self):
            steps = []
            for i in self.items:
                steps.append(i.text())
            self.steps_str = ''
            for i in steps:
                self.steps_str = self.steps_str + " " + i + ','
            steps_session.append(self.steps_str)"""


class SignUp:
    def __init__(self):
        self.con = sqlite3.connect("database/database.db")

    def user_exists(self, username):
        with self.con as db:
            cur = db.cursor()
            cur.execute("SELECT username FROM usersdata")
            names = {name[0] for name in cur.fetchall()}
            if username in names:
                return True
        return False


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect("database/database.db")

    def database_sign_up(self, username, password):
        with self.con as db:
            cur = db.cursor()
            cur.execute('INSERT INTO usersdata(username, password) VALUES (?, ?)',
                        Tasks().func_user_info(username, password))

    def database_add_task(self):
        username = username_session[0]
        content = content_session[0]
        with self.con as db:
            status = 'ongoing'
            #d = input('Введите дату (ГГГГ-ММ-ДД): ')
            #date = datetime.strptime(d, '%Y-%m-%d')
            cur = db.cursor()
            status_time = time.ctime()
            d = date[0].toPyDate()
            #for i in steps_session:
                #if not i:
                    #steps_session.remove(i)
            #steps = "ddd"
            print('iz db', steps_session[0])
            steps = steps_session[0]
            if steps_session:
                cur.execute(
                    'INSERT INTO userstasks(username, date, content, status, status_time) VALUES (?, ?, ?, ?, ?)',
                    (username, d, content, status, time.ctime()))
            else:
                cur.execute(
                    'INSERT INTO userstasks(username, date, content, steps, status, status_time) VALUES (?, ?, ?, ?, ?,'
                    ' ?)',
                    (username, d, content, steps_session[0], status, time.ctime()))

    def database_all_tasks(self, username):
        with self.con as db:
            row_list = []
            cur = db.cursor()
            execute = cur.execute('SELECT * from userstasks WHERE username = ?',
                                  (Tasks().func_username_container(username)))
            if not Tasks().tasks_exists(username):
                for row in execute:
                    row_list.append(row)
                return row_list
            else:
                print("Not a single task was found")

    def database_task_status(self, username, status_choice, password):
        status = []
        with self.con as db:
            cur = db.cursor()
            execute = cur.execute('SELECT date from userstasks WHERE username = ?',
                                  (Tasks().func_username_container(username)))
            if status_choice == '1':
                if Tasks().tasks_exists(username):
                    for row in execute:
                        cur.execute('SELECT * from userstasks WHERE username = ? ',
                                    (Tasks().func_username_container(username)))
                        task_date = cur.fetchall()
                        for i in task_date:
                            d = time.localtime()
                            getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                            t1 = datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S")
                            t2 = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                            time_diff = abs(t1 - t2)
                            if time_diff > timedelta(days=3):
                                status.append(i)
                if status:
                    pprint.pprint(status)
                else:
                    print('Просроченных задач не нашлось!')
                TaskManager().task_manager(username, password)
            elif status_choice == '2':
                if Tasks().compare_data(username, password):
                    for row in execute:
                        cur.execute('SELECT * from userstasks WHERE username = ?',
                                    (Tasks().func_username_container(username)))
                        task_date = cur.fetchall()
                        for i in task_date:
                            d = time.localtime()
                            getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                            t3 = datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S")
                            t4 = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                            time_diff = abs(t3 - t4)
                            if time_diff < timedelta(days=1):
                                status.append(i)
                if status:
                    pprint.pprint(status)
                else:
                    print('Задач на сегодня не нашлось!')
                TaskManager().task_manager(username, password)

            elif status_choice == '3':
                if Tasks().compare_data(username, password):
                    for row in execute:
                        cur.execute('SELECT * from userstasks WHERE username = ?',
                                    (Tasks().func_username_container(username)))
                        task_date = cur.fetchall()
                        for i in task_date:
                            d = time.localtime()
                            getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                            t5 = datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S")
                            t6 = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                            time_diff = t6 - t5
                            if time_diff < timedelta(days=3):
                                status.append(i)
                if status:
                    pprint.pprint(status)
                else:
                    print('Задач на ближайшие 3 дня не нашлось!')
                TaskManager().task_manager(username, password)

    def database_update_status(self, username, password):
        with self.con as db:
            cur = db.cursor()
            d = time.localtime()
            getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
            t = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
            execute = cur.execute('SELECT date from userstasks WHERE username = ?',
                                  (Tasks().func_username_container(username)))
            for row in execute:
                cur.execute('SELECT * from userstasks WHERE username = ?',
                            (Tasks().func_username_container(username)))
                task_date = cur.fetchall()
                for row, count in enumerate(task_date, start=1):
                    print("|", row, "|", 'Задача:', count[3], '| Статус: ', count[5], '|')
            choice = int(input('Выберите номер задачи, который желаете изменить\n'))
            print('Вы выбрали задачу № ', choice)
            choice2 = (input('Изменить на завершено, или отменено?\n'))

            if choice2.lower() == 'завершено':
                update_variables = 'completed', username, choice
                cur.execute('UPDATE userstasks SET status = ? WHERE username = ? AND tid = ?',
                            update_variables)
            elif choice2.lower() == 'отменено':
                update_variables = 'cancelled', username, choice
                cur.execute('UPDATE userstasks SET status = ? WHERE username = ? AND tid = ?',
                            update_variables)
            else:
                print('Введите завершено или отменено!')
            TaskManager().task_manager(username, password)

    def database_task_exists(self, username):
        with self.con as db:
            cur = db.cursor()
            cur.execute('SELECT * from userstasks ')
            names = {name[0] for name in cur.fetchall()}
            if username in names:
                return True

    def database_compare_data(self, username, password):
        with self.con as db:
            cur = db.cursor()
            cur.execute("SELECT username, password FROM usersdata")
            data_list = cur.fetchall()
            for i in data_list:
                if Tasks().func_user_input(username, password) == i:
                    return True
        return False


class Tasks:
    def __init__(self):
        self.con = sqlite3.connect("database/database.db")

    def tasks_status(self, username, password):
        print('Задачи по статусу \n1- Просроченные задачи \n2- Задачи на сегодня \n3- Задачи на 3 дня')
        status_choice = input('Введите пункт: ')
        DataBase().database_task_status(username, password, status_choice)

    def update_status(self, username: str, password: str):
        if self.tasks_exists(username):
            print('Задачи пользователя', username)
            DataBase().database_update_status(username, password)
        else:
            print('У пользователя нет задач')
            TaskManager().task_manager(username, password)
        TaskManager().task_manager(username, password)

    def tasks_exists(self, username):
        DataBase().database_task_exists(username)
        return False

    def func_username_container(self, username):
        username_container = [username]
        return username_container

    def func_user_info(self, username, password):
        user_info = (username, password)
        return user_info

    def func_user_input(self, username, password):
        user_input = (username, password)
        return user_input

    def compare_data(self, username, password):
        return DataBase().database_compare_data(username, password)

    def return_function(self, choice):
        funcctions = {
            1: self.__getattribute__("all_tasks"),
            2: self.__getattribute__("add_task"),
            3: self.__getattribute__("tasks_status"),
            4: self.__getattribute__("update_status"),
            5: TaskManager().__getattribute__("main")
        }
        return funcctions.get(int(choice))


class TaskManager:

    def __init__(self, user_name=None, db=None):
        self.username = user_name
        self.create_structure()
        self.con = sqlite3.connect("database/database.db")  # используем далее self.con
        # self.cur = db.cursor()

    @staticmethod
    def create_structure():
        os.makedirs('datafiles', exist_ok=True)
        os.makedirs('database', exist_ok=True)

    # def data_files(self):
    #     if not os.path.isdir("database"):
    #         os.mkdir("database")

    def data_files_tasks(self):
        with self.con as db:
            db.executescript(if_not_exists)

    def main(self, password=None, username=None):
        os.system('cls')
        print("Меню")
        choice = input("1 - Вход \n2 - Регистрация \n3 - Выход \nВыберите пункт: ")
        self.return_function_for_main(choice)()

    def return_function_for_main(self, choice):
        funcctions = {
            1: self.__getattribute__("log_in"),
            2: SignUp().__getattribute__("sign_up"),
            3: self.__getattribute__("exitt"),
        }
        return funcctions.get(int(choice))


if __name__ == "__main__":
    # manager = TaskManager(user_name="awfawafgrg")
    # manager.data_files()
    # manager.data_files_tasks()
    # manager.main()
    app = QApplication(sys.argv)
    style = """
        QWidget{
            background: #262D37;
        }
        QLabel{
            color: #D3D3D3;
        }
        QLineEdit{
            border: 2px solid #D3D3D3;
            border-radius: 8px;
            padding: 1px;
            color: #D3D3D3;
        }
        QPushButton{
            color: #D3D3D3;
            background: #808080;
            border: 1px #DADADA solid;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: bold;
            font-size: 9pt;
            outline: none
        }
        
    """
    username_session = []
    password_session = []
    content_session = []
    date = []
    steps_session = []
    app.setStyleSheet(style)
    MW = MainWindow()
    MW.setWindowTitle("Task manager")
    MW.setFixedSize(400, 300)
    MW.show()
    sys.exit(app.exec_())
