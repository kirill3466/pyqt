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
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout


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
        window2 = LogInWindow()
        widget.addWidget(window2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def go_to_signup(self):
        window3 = SignUpWindow()
        widget.addWidget(window3)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class LogInWindow(QWidget):
    def __init__(self):
        super(LogInWindow, self).__init__()
        self.usernameLabel = QtWidgets.QLabel("Username")
        self.passwordLabel = QtWidgets.QLabel("Password")
        self.backButton = QtWidgets.QPushButton('Back')
        self.loginButton = QtWidgets.QPushButton('Log in')
        self.errorLabel = QtWidgets.QLabel('The email or password is incorrect.')
        self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()
        self.backButton.clicked.connect(self.go_back)
        self.errorLabel.setStyleSheet("color : 'red'")
        self.passwordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.login_function)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        #buttonLayout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
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

    def go_back(self):
        os.system('cls')
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def login_function(self):
        username = self.usernameLine.text()
        password = self.passwordLine.text()
        print(username)
        print(password)
        if len(username) == 0 or len(password) == 0:
            self.errorLabel.setText("Please input all fields.")
            self.errorLabel.show()
        else:
            if SignUp().user_exists(username):
                if Tasks().compare_data(username, password):
                    print("Successfully logged in.")
                    self.errorLabel.setText("")
                    self.go_to_task_manager()
                else:
                    self.errorLabel.setText("Invalid username or password")
                    self.errorLabel.show()
            else:
                self.errorLabel.setText("User not found")
                self.errorLabel.show()

    def go_to_task_manager(self):
        pass

class SignUpWindow(QWidget):
    def __init__(self):
        super(SignUpWindow, self).__init__()
        self.usernameLabel = QtWidgets.QLabel("Username")
        self.passwordLabel = QtWidgets.QLabel("Password")
        self.passwordLabel2 = QtWidgets.QLabel("Confirm password")
        self.backButton = QtWidgets.QPushButton('Back')
        self.loginButton = QtWidgets.QPushButton('Log in')
        self.usernameLine = QtWidgets.QLineEdit()
        self.passwordLine = QtWidgets.QLineEdit()
        self.passwordLine2 = QtWidgets.QLineEdit()
        self.errorLabel = QtWidgets.QLabel('ERROR')
        self.errorLabel.setStyleSheet("color : 'red'")
        self.backButton.clicked.connect(self.go_back)
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
        layout.addWidget(self.passwordLine2)
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.loginButton)
        layout.addWidget(self.backButton)
        self.errorLabel.hide()
        self.setLayout(layout)

    def go_back(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

class TaskManagerUI(QWidget):
    pass

class SignUp:
    def __init__(self):
        self.con = sqlite3.connect("database/database.db")

    def sign_up(self):
        os.system('cls')
        print("Введите имя и пароль для регистрации")
        username = input("Введите имя: ")
        password = input("Введите пароль: ")
        password1 = input('Подтвердите пароль: ')
        Tasks().compare_data(username, password)
        if password != password1:
            print("Пароли не совпадают!")
            TaskManager().main()
        else:
            if self.user_exists(username):
                print("Такой пользователь уже существует")
            else:
                DataBase().database_sign_up(username, password)
                print('Регистрация прошла успешно!')
        TaskManager().main()

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

    def database_add_task(self, username):
        with self.con as db:
            status = 'ongoing'
            content = input('Введите задачу, которую хотите добавить в список:\n ')
            d = input('Введите дату (ГГГГ-ММ-ДД): ')
            date = datetime.strptime(d, '%Y-%m-%d')
            steps = 'NULL'
            cur = db.cursor()
            option = input(
                'Нужно ли добавить шаги ? \n<Enter>, чтобы пропустить добавление шагов \n''да'', если добавить \n')
            if len(option) > 1:
                if option.lower() == 'да':
                    j = int(input('Введите сколько шагов нужно добавить: '))
                    steps = []
                    for i in range(1, j + 1):
                        step = input("Введите шаг :")
                        steps.append(step)
                    steps_string = ', '.join([str(item) for item in steps])
                elif option == 'нет' or len(option) < 1 or 'Нет':
                    steps = 'NULL'
            if steps == 'NULL':
                cur.execute(
                    'INSERT INTO userstasks(username, date, content, status, status_time) VALUES (?, ?, ?, ?, ?)',
                    (username, date, content, status, time.ctime()))
            else:
                cur.execute(
                    'INSERT INTO userstasks(username, date, content, steps, status, status_time) VALUES (?, ?, ?, ?, ?,'
                    ' ?)',
                    (username, date, content, steps_string, status, time.ctime()))

    def database_all_tasks(self, username, execute):
        with self.con as db:
            cur = db.cursor()
            execute = cur.execute('SELECT * from userstasks WHERE username = ?',
                                  (Tasks().func_username_container(username)))
            if Tasks().tasks_exists(username):
                for row in execute:
                    print(row)
            else:
                print("У пользователя нет никаких задач!")

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

    def add_task(self, username, password):
        # tid = str(uuid.uuid4().fields[-1])[:5]
        DataBase().database_add_task(username)
        TaskManager().task_manager(username, password)

    def all_tasks(self, username, password):
        print('Текущие задачи пользователя', username)
        DataBase().database_all_tasks(username, password)
        TaskManager().task_manager(username, password)

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
        DataBase().database_compare_data(username, password)

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

    def exitt(self):
        sys.exit()

    def task_manager(self, username, password):
        print('Привет, ', username)
        print(
            "Менеджер задач \n1 - Все задачи \n2 - Добавить задачи \n3 - Задачи по статусу \n4 - Обновить статус задачи"
            " \n5 - Возврат в меню")
        choice = input('Введите пункт: ')
        Tasks().return_function(choice)(username, password)
        os.system('cls')

    def log_in(self):
        os.system('cls')
        print('Введите данные для входа')
        username = input('Имя: ')
        password = input('Пароль: ')
        if SignUp().user_exists(username):
            if Tasks().compare_data(username, password):
                print('Вы успешно вошли!')
                self.task_manager(username, password)
            else:
                print('Введите корректные данные')
                self.main()
        else:
            print('Пользователь не найден')
            self.main()


if __name__ == "__main__":
    # manager = TaskManager(user_name="awfawafgrg")
    # manager.data_files()
    # manager.data_files_tasks()
    # manager.main()
    app = QApplication(sys.argv)
    window = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(window)
    widget.setWindowTitle("Task manager")
    widget.setFixedSize(400, 300)
    widget.show()
    sys.exit(app.exec_())
