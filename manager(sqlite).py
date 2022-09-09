import json
import os
import datetime
import time
import sys
from datetime import datetime 
from datetime import timedelta
import os.path
import uuid
import pprint
import sqlite3
from database_query import if_not_exists

class TaskManager:

    def __init__(self, user_name = None):
        self.username = user_name
        self.database = ""

    def data_files(self):
        if not os.path.isdir("database"):
            os.mkdir("database")

    def data_files_tasks(self):
        with sqlite3.connect("database/database.db") as db:
            cur = db.cursor()

            cur.executescript(if_not_exists)
    def connect_function(self, username, password):
                with sqlite3.connect("database/database.db") as db:
                    cur = db.cursor()
                    username_container = [username]
                    user_info = [username, password]

    def main(self, choice=None, password=None, username=None ):
        os.system('cls')
        print("Меню")
        choice = input("1 - Вход \n2 - Регистрация \n3 - Выход \nВыберите пункт: ")
        self.return_function_for_main(choice, username, password)

    def return_function_for_main(self, choice, username, password):
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
        os.system('cls')
        print('Привет, ', username)
        print("Менеджер задач \n1 - Все задачи \n2 - Добавить задачи \n3 - Задачи по статусу \n4 - Обновить статус задачи \n5 - Возврат в меню")
        choice = input('Введите пункт: ')
        self.return_function(choice, username, password)
        os.system('cls')


    def add_task(self, username, password):
            #tid = str(uuid.uuid4().fields[-1])[:5]
            with sqlite3.connect("database/database.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as db:
                cur = db.cursor()
                status_time = time.ctime()
                status = 'ongoing'
                content = input('Введите задачу, которую хотите добавить в список:\n ')
                d = input('Введите дату (ГГГГ-ММ-ДД): ')
                date = datetime.strptime(d, '%Y-%m-%d')
                steps = 'NULL'
                option = input('Нужно ли добавить шаги ? \n<Enter>, чтобы пропустить добавление шагов \n''да'', если добавить \n')
                if len(option)>1 :
                    if option.lower() == 'да':
                        j = int(input('Введите сколько шагов нужно добавить: '))
                        steps = []
                        for i in range(1, j+1):
                            step = input("Введите шаг :")
                            steps.append(step)
                        steps_string = ', '.join([str(item) for item in steps])
                    elif option == 'нет' or len(option)<1 or 'Нет':
                        steps = 'NULL'
                if steps == 'NULL':
                    cur.execute('INSERT INTO userstasks(username, date, content, status, status_time) VALUES (?, ?, ?, ?, ?)', (username, date, content, status, time.ctime()))
                else:
                    cur.execute('INSERT INTO userstasks(username, date, content, steps, status, status_time) VALUES (?, ?, ?, ?, ?, ?)', (username, date, content, steps_string, status, time.ctime()))
            self.task_manager(username, password)

            
    def all_tasks(self, username, password):
        
            print('Текущие задачи пользователя',username)
            
            with sqlite3.connect("database/database.db") as db:
                cur = db.cursor()
                username_container = [username]
                execute = cur.execute('SELECT * from userstasks WHERE username = ?', (username_container))
                if self.tasks_exists(username, password):
                    for row in execute:
                        print(row)
                else:
                    print("У пользователя нет никаких задач!")
            self.task_manager(username,password)

    @staticmethod
    def func_for_status(t1, t2):
        return any(t1 <= t2)


    def tasks_status(self, username, password):
            print('Задачи по статусу \n1- Просроченные задачи \n2- Задачи на сегодня \n3- Задачи на 3 дня')
            status_choice = input('Введите пункт: ')
            message = None
            status = []

            with sqlite3.connect("database/database.db") as db:
                cur = db.cursor()
                username_container = [username]
                execute = cur.execute('SELECT date from userstasks WHERE username = ?', (username_container))
                if status_choice == '1':
                        if self.tasks_exists(username, password):
                            for row in execute:
                                cur.execute('SELECT * from userstasks WHERE username = ? ', (username_container))
                                task_date = cur.fetchall()
                                for i in task_date:
                                    d = time.localtime()
                                    getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                                    t1 = datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S")
                                    t2 = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                                    time_diff = abs(t1-t2)
                                    if time_diff > timedelta(days = 3):
                                                status.append(i)     
                        if status:
                            pprint.pprint(status)
                        else:
                            print('Просроченных задач не нашлось!')
                        self.task_manager(username,password)
                elif status_choice == '2':
                        if self.compare_data(username, password):
                            for row in execute:
                                cur.execute('SELECT * from userstasks WHERE username = ?', (username_container))
                                task_date = cur.fetchall()
                                for i in task_date:
                                    d = time.localtime()
                                    getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                                    t3 = datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S")
                                    t4 = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                                    time_diff = abs(t3-t4)
                                    if time_diff < timedelta(days = 1):
                                        status.append(i)
                        if status:
                            pprint.pprint(status)
                        else:
                            print('Задач на сегодня не нашлось!')
                        self.task_manager(username,password)
                       
                elif status_choice == '3':
                        if self.compare_data(username, password) == True:
                            for row in execute:
                                cur.execute('SELECT * from userstasks WHERE username = ?', (username_container))
                                task_date = cur.fetchall()
                                for i in task_date:
                                    d = time.localtime()
                                    getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                                    t5 = datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S")
                                    t6 = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                                    time_diff = t6-t5
                                    if time_diff < timedelta(days = 3):
                                        status.append(i)
                        if status:
                            pprint.pprint(status)
                        else:
                            print('Задач на ближайшие 3 дня не нашлось!')
                        self.task_manager(username, password)

    def update_status(self, username: str, password: str):
        if self.tasks_exists(username, password):
            print('Задачи пользователя',username)
            with sqlite3.connect("database/database.db") as db:
                cur = db.cursor()
                username_container = [username]
                d = time.localtime()
                getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                t = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                
                execute = cur.execute('SELECT date from userstasks WHERE username = ?', (username_container))
                for row in execute:
                                cur.execute('SELECT * from userstasks WHERE username = ?', (username_container))
                                task_date = cur.fetchall()
                                for row, count in enumerate(task_date, start = 1):
                                    print("|",row,"|", 'Задача:', count[3],'| Статус: ', count[5], '|')
                choice = int(input('Выберите номер задачи, который желаете изменить\n'))
                print('Вы выбрали задачу № ', choice)
                choice2 = (input('Изменить на завершено, или отменено?\n'))
                
                if choice2.lower() == 'завершено':
                    update_variables = 'completed', username, choice
                    cur.execute('UPDATE userstasks SET status = ? WHERE username = ? AND tid = ?', update_variables)
                elif choice2.lower() == 'отменено':
                    update_variables = 'cancelled', username, choice
                    cur.execute('UPDATE userstasks SET status = ? WHERE username = ? AND tid = ?', update_variables)
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
            with sqlite3.connect("database/database.db") as db:
                    cur = db.cursor()
                    user_info = [username, password]
                    if self.user_exists(username, password):
                        print("Такой пользователь уже существует")
                    else:
                        cur.execute('INSERT INTO usersdata(username, password) VALUES (?, ?)', user_info)
                        print('Регистрация прошла успешно!')
            self.main()

        
    def tasks_exists(self, username, password):
        with sqlite3.connect("database/database.db") as db:
            cur = db.cursor()
            cur.execute('SELECT * from userstasks ')
            names = {name[0] for name in cur.fetchall()}
            if username in names:
                return True
    
    def user_exists(self, username, password):
        with sqlite3.connect("database/database.db") as db:
            cur = db.cursor()
            cur.execute("SELECT username FROM usersdata")
            names = {name[0] for name in cur.fetchall()}
            if username in names:
                return True




    def compare_data(self, username, password):
        with sqlite3.connect("database/database.db") as db:
            user_input = (username, password)
            cur = db.cursor()
            cur.execute("SELECT username, password FROM usersdata")
            data_list = cur.fetchall()
            for i in data_list:
                if user_input == i:
                    return True
                            
    def log_in(self):
        os.system('cls')
        print('Введите данные для входа')
        username = input('Имя: ')
        password = input('Пароль: ')
        if self.user_exists(username, password):
            if self.compare_data(username, password):
                print('Вы успешно вошли!')
                self.task_manager(username,password)
            else:
                print('Введите корректные данные')
                self.main()
        else:
            print('Пользователь не найден')
            self.main()
            

if __name__ == "__main__":
    manager = TaskManager(user_name="awfawafgrg")
    manager.data_files()
    manager.data_files_tasks()
    manager.main()
    
