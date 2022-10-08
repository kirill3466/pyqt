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
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


class TaskManager:
    class User:
        def __init__(self, username, password, uid):
            self.uid = uid
            self.username = username
            self.password = password

        def check_password_length(self):
            if len(self.password) < 4:
                raise ValueError('Слабый пароль')

    class Task:
        def __init__(self, username, date, content, steps, status):
            self.username = username
            self.date = date
            self.content = content
            self.steps = steps
            self.status = status

    class Database:
        pass

    def data_files():
        if not os.path.isdir("datafiles"):
            os.mkdir("datafiles")

    def data_files_tasks():
        if not os.path.isfile("datafiles/datatasks.json"):
            open("datafiles/datatasks.json", 'w')
        size = os.path.getsize('datafiles/datatasks.json')
        if size > 0:
            pass
        else:
            tasks_data = {
                "userstasks": []
            }
            with open("datafiles/datatasks.json", 'w') as file:
                json.dump(tasks_data, file, indent=4, default=str)

    def data_files_users():

        if not os.path.isfile("datafiles/data.json"):
            open("datafiles/data.json", 'w')
        else:
            pass

        size = os.path.getsize('datafiles/data.json')
        if size > 0:
            pass
        else:
            data = {
                'userinfo': []
            }
            with open("datafiles/data.json", 'w') as file:
                json.dump(data, file, indent=2)

    def main(choice=None):
        os.system('cls')
        print("Меню")
        choice = input("1 - Вход \n2 - Регистрация \n3 - Выход \nВыберите пункт: ")
        if choice == "1":
            print('Введите данные для входа')
            username = str(input('Имя: '))
            password = str(input('Пароль: '))
            TaskManager.log_in(username, password)
        elif choice == "2":
            os.system('cls')
            print("Введите имя и пароль для регистрации")
            username = str(input("Введите имя: "))
            password = str(input("Введите пароль: "))
            password1 = str(input('Подтвердите пароль: '))
            if password != password1:
                print("Пароли не совпадают!")
                TaskManager.main()
            else:
                TaskManager.sign_up(username, password, uid=None)
        elif choice == "3":
            TaskManager.exitt()

    def exitt():
        sys.exit()

    def task_manager(username, password):
        os.system('cls')
        print('Привет, ', username)
        print(
            "Менеджер задач \n1 - Все задачи \n2 - Добавить задачи \n3 - Задачи по статусу \n4 - Обновить статус задачи \n5 - Возврат в меню")
        choice = input('Введите пункт: ')
        if choice == '1':
            TaskManager.all_tasks(username, password)
        elif choice == '2':
            TaskManager.add_task(username, password)
        elif choice == '3':
            TaskManager.tasks_status(username, password)
        elif choice == '4':
            TaskManager.update_status(username, password)
        elif choice == '5':
            TaskManager.main()
        os.system('cls')

    def add_task(username, password):

        tid = str(uuid.uuid4().fields[-1])[:5]
        tasks_data = {
            "userstasks": []
        }
        status_time = time.ctime()
        status = ["ongoing", status_time]
        content = str(input('Введите задачу, которую хотите добавить в список:\n '))
        d = input('Введите дату (ГГГГ-ММ-ДД): ')
        date = datetime.strptime(d, '%Y-%m-%d')
        steps = None
        option = input(
            'Нужно ли добавить шаги ? \n<Enter>, чтобы пропустить добавление шагов \n''да'', если добавить \n')
        if len(option) > 1:
            if option.lower() == 'да':
                j = int(input('Введите сколько шагов нужно добавить: '))
                steps = []
                for i in range(1, j + 1):
                    step = input("Введите шаг :")
                    steps.append(step)
                print(steps)
            elif option == 'нет' or len(option) < 1 or 'Нет':
                steps = None

        with open('datafiles/datatasks.json', 'r') as file:
            for i in tasks_data:
                tasks_data = json.load(file)
                tasks_data["userstasks"].append(TaskManager.Task(username, date, content, steps, status).__dict__)
                with open("datafiles/datatasks.json", 'w') as outfile:
                    json.dump(tasks_data, outfile, indent=4, default=str)
        TaskManager.task_manager(username, password)

    def all_tasks(username, password):
        print('Текущие задачи пользователя', username)
        all_tasks_list = []
        message = None
        with open("datafiles/datatasks.json") as f:
            tasks_data = json.load(f)
        if len(tasks_data['userstasks']) != 0:
            for i in tasks_data["userstasks"]:
                if username == i["username"]:
                    all_tasks_list.append(i)
        else:
            message = 'У пользователя нет никаких задач!'
        if message != None:
            print(message)
        else:
            pprint.pprint(all_tasks_list)

        TaskManager.task_manager(username, password)

    def tasks_status(username, password):
        print('Задачи по статусу \n1- Просроченные задачи \n2- Задачи на сегодня \n3- Задачи на 3 дня')
        status_choice = input('Введите пункт: ')
        message = None
        status = []

        def func_for_status(t1, t2):
            return any(t1 <= t2)

        with open("datafiles/datatasks.json") as f:
            tasks_data = json.load(f)
            if status_choice == '1':
                if TaskManager.compare_data(username, password) == True:
                    for i in tasks_data['userstasks']:
                        d = time.localtime()
                        getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                        t1 = datetime.strptime(i['date'], "%Y-%m-%d %H:%M:%S")
                        t2 = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                        time_diff = abs(t1 - t2)
                        if time_diff > timedelta(days=3):
                            status.append(i)
                        else:
                            message = 'Просроченных задач не нашлось!'
                if status:
                    pprint.pprint(status)
                else:
                    print(message)
                TaskManager.task_manager(username, password)



            elif status_choice == '2':
                if TaskManager.compare_data(username, password) == True:
                    for i in tasks_data['userstasks']:
                        d = time.localtime()
                        getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                        t3 = datetime.strptime(i['date'], "%Y-%m-%d %H:%M:%S")
                        t4 = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                        time_diff = abs(t3 - t4)
                        if time_diff < timedelta(days=1):
                            status.append(i)
                        else:
                            message = 'Задач на сегодня не нашлось!'
                if status:
                    pprint.pprint(status)
                else:
                    print(message)
                TaskManager.task_manager(username, password)

            elif status_choice == '3':
                if TaskManager.compare_data(username, password) == True:
                    for i in tasks_data['userstasks']:
                        d = time.localtime()
                        getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                        t5 = datetime.strptime(i['date'], "%Y-%m-%d %H:%M:%S")
                        t6 = datetime.strptime(getctime, "%Y-%m-%d %H:%M:%S")
                        time_diff = t6 - t5
                        if time_diff < timedelta(days=0) and time_diff < timedelta(days=3):
                            status.append(i)
                        else:
                            message = 'Задач на ближайшие 3 дня не нашлось!'
                if status:
                    pprint.pprint(status)
                else:
                    print(message)
                TaskManager.task_manager(username, password)

    def update_status(username, password):
        if TaskManager.tasks_exists(username, password) == True:
            print('Задачи пользователя', username)
            with open("datafiles/datatasks.json") as f:
                tasks_data = json.load(f)
            count_list = []
            list_for_selection = []
            dictionary_for_selection = {}
            for count, i in enumerate(tasks_data["userstasks"], start=1):
                print("|", count, "|", i['content'], i['status'])
            choice = int(input('Выберите номер задачи, который желаете изменить\n')) - 1
            for count, i in enumerate(tasks_data["userstasks"]):
                count_list.append(count)
                list_for_selection.append(i['content'])
                dictionary_for_selection = dict(zip(count_list, list_for_selection))
                for y in dictionary_for_selection.keys():
                    if y == choice:
                        choice2 = input("Изменить на завершено, или отменено?\n")
                        if choice2.lower() == 'завершено':
                            d = time.localtime()
                            getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                            i['status'][0] = "completed"
                            i['status'][1] = getctime
                            with open("datafiles/datatasks.json", 'w') as outfile:
                                json.dump(tasks_data, outfile, indent=4)
                            TaskManager.task_manager(username, password)
                        elif choice2.lower() == 'отменено':
                            d = time.localtime()
                            getctime = time.strftime('%Y-%m-%d %H:%M:%S', d)
                            i['status'][0] = "cancelled"
                            i['status'][1] = getctime
                            with open("datafiles/datatasks.json", 'w') as outfile:
                                json.dump(tasks_data, outfile, indent=4)
                            TaskManager.task_manager(username, password)
                        else:
                            print('Введите завершено или отменено!')
                            TaskManager.task_manager(username, password)
        else:
            print('У пользователя нет задач!')

        TaskManager.task_manager(username, password)

    def sign_up(username, password, uid=None):
        os.system('cls')
        data = {
            'userinfo': []
        }
        uid = str(uuid.uuid4())
        with open('datafiles/data.json', 'r') as file:
            data = json.load(file)
            if TaskManager.user_exists(username, password) == True:
                print('Такой пользователь  уже существует')
            else:
                for i in data:
                    data['userinfo'].append(TaskManager.User(username, password, uid).__dict__)
                    with open('datafiles/data.json', 'w') as outfile:
                        json.dump(data, outfile, indent=2)
                        print('Регистрация прошла успешно!')
            TaskManager.main()

    def tasks_exists(username, password):
        with open('datafiles/datatasks.json', 'r') as file:
            check = json.load(file)
        return any((username == i['username']) for i in check['userstasks'])

    def user_exists(username, password):
        with open('datafiles/data.json', 'r') as file:
            check = json.load(file)
        return any((username == i['username']) for i in check['userinfo'])

    def compare_data(username, password):
        with open('datafiles/data.json', 'r') as file:
            check = json.load(file)
        for i in check['userinfo']:
            if username == i['username'] and password == i['password']:
                return True

    def log_in(username, password):
        os.system('cls')
        with open('datafiles/data.json') as f:
            info = json.load(f)
        message = 'Пользователь не найден!'
        if TaskManager.user_exists(username, password) == True:
            if TaskManager.compare_data(username, password) == True:
                print('Вы успешно вошли!')
                TaskManager.task_manager(username, password)
            else:
                print('Введите корректные данные')
                TaskManager.main()
        else:
            print('Пользователь не найден')
            TaskManager.main()


if __name__ == "__main__":
    TaskManager.data_files()
    TaskManager.data_files_users()
    TaskManager.data_files_tasks()
    TaskManager.main()
