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

    def func_username_container(self, username):
        username_container = [username]
        return username_container

    def func_user_info(self, username, password):
        user_info = (username, password)
        return user_info

    def func_user_input(self, username, password):
        user_input = (username, password)
        return user_input

    def main(self, password=None, username=None):
        os.system('cls')
        print("Меню")
        choice = input("1 - Вход \n2 - Регистрация \n3 - Выход \nВыберите пункт: ")
        self.return_function_for_main(choice)
        # Функция return_function_for_main принимает только choice, а ты передаешь еще два аргумента.
        # В других местах тоже много ошибок с передачей.

    def return_function_for_main(self, choice):
        funcctions = {
            1: self.log_in(),
            2: self.sign_up(),
            3: self.exitt(),
        }
        return funcctions.get(int(choice))

    def exitt(self):
        sys.exit()

    def return_function(self, choice, username, password):
        funcctions = {
            1: self.all_tasks(username, password),
            2: self.add_task(username, password),
            3: self.tasks_status(username, password),
            4: self.update_status(username, password),
            5: self.main()
        }
        return funcctions.get(int(choice))

    def task_manager(self, username, password):
        print('Привет, ', username)
        print(
            "Менеджер задач \n1 - Все задачи \n2 - Добавить задачи \n3 - Задачи по статусу \n4 - Обновить статус задачи"
            " \n5 - Возврат в меню")
        choice = input('Введите пункт: ')
        self.return_function(choice, username, password)
        os.system('cls')

    def add_task(self, username, password):
        # tid = str(uuid.uuid4().fields[-1])[:5]
        with self.con as db:
            cur = db.cursor()
            status = 'ongoing'
            content = input('Введите задачу, которую хотите добавить в список:\n ')
            d = input('Введите дату (ГГГГ-ММ-ДД): ')
            date = datetime.strptime(d, '%Y-%m-%d')
            steps = 'NULL'
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
        self.task_manager(username, password)

    def all_tasks(self, username, password):

        print('Текущие задачи пользователя', username)
        with self.con as db:
            cur = db.cursor()
            execute = cur.execute('SELECT * from userstasks WHERE username = ?',
                                  (self.func_username_container(username)))
            if self.tasks_exists(username):
                for row in execute:
                    print(row)
            else:
                print("У пользователя нет никаких задач!")
        self.task_manager(username, password)

    def tasks_status(self, username, password):
        print('Задачи по статусу \n1- Просроченные задачи \n2- Задачи на сегодня \n3- Задачи на 3 дня')
        status_choice = input('Введите пункт: ')
        status = []

        with self.con as db:
            cur = db.cursor()
            execute = cur.execute('SELECT date from userstasks WHERE username = ?',
                                  (self.func_username_container(username)))
            if status_choice == '1':
                if self.tasks_exists(username):
                    for row in execute:
                        cur.execute('SELECT * from userstasks WHERE username = ? ',
                                    (self.func_username_container(username)))
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
                self.task_manager(username, password)
            elif status_choice == '2':
                if self.compare_data(username, password):
                    for row in execute:
                        cur.execute('SELECT * from userstasks WHERE username = ?',
                                    (self.func_username_container(username)))
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
                self.task_manager(username, password)

            elif status_choice == '3':
                if self.compare_data(username, password):
                    for row in execute:
                        cur.execute('SELECT * from userstasks WHERE username = ?',
                                    (self.func_username_container(username)))
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
                self.task_manager(username, password)

    def update_status(self, username: str, password: str):
        if self.tasks_exists(username):
            print('Задачи пользователя', username)
            with self.con as db:
                cur = db.cursor()
                d = time.localtime()
                getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                t = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                execute = cur.execute('SELECT date from userstasks WHERE username = ?',
                                      (self.func_username_container(username)))
                for row in execute:
                    cur.execute('SELECT * from userstasks WHERE username = ?',
                                (self.func_username_container(username)))
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
                self.task_manager(username, password)
        else:
            print('У пользователя нет задач')
            self.task_manager(username, password)
        self.task_manager(username, password)

    def sign_up(self):
        os.system('cls')
        print("Введите имя и пароль для регистрации")
        username = input("Введите имя: ")
        password = input("Введите пароль: ")
        password1 = input('Подтвердите пароль: ')
        self.compare_data(username, password)
        if password != password1:
            print("Пароли не совпадают!")
            self.main()
        else:
            with self.con as db:
                cur = db.cursor()
                if self.user_exists(username):
                    print("Такой пользователь уже существует")
                else:
                    cur.execute('INSERT INTO usersdata(username, password) VALUES (?, ?)',
                                self.func_user_info(username, password))
                    print('Регистрация прошла успешно!')
            self.main()

    def tasks_exists(self, username):
        with self.con as db:
            cur = db.cursor()
            cur.execute('SELECT * from userstasks ')
            names = {name[0] for name in cur.fetchall()}
            if username in names:
                return True
        return False

    def user_exists(self, username):
        with self.con as db:
            cur = db.cursor()
            cur.execute("SELECT username FROM usersdata")
            names = {name[0] for name in cur.fetchall()}
            if username in names:
                return True
        return False

    def compare_data(self, username, password):
        with self.con as db:
            cur = db.cursor()
            cur.execute("SELECT username, password FROM usersdata")
            data_list = cur.fetchall()
            for i in data_list:
                if self.func_user_input(username, password) == i:
                    return True
        return False

    def log_in(self):
        os.system('cls')
        print('Введите данные для входа')
        username = input('Имя: ')
        password = input('Пароль: ')
        if self.user_exists(username):
            if self.compare_data(username, password):
                print('Вы успешно вошли!')
                self.task_manager(username, password)
            else:
                print('Введите корректные данные')
                self.main()
        else:
            print('Пользователь не найден')
            self.main()


if __name__ == "__main__":
    manager = TaskManager(user_name="awfawafgrg")
    # manager.data_files()
    manager.data_files_tasks()
    manager.main()
