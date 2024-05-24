# импорт библиотек
import time
from tkinter import *
import sqlite3
from tkinter.messagebox import *
import datetime
import hashlib

error_input = 0
block = 0
user = 0
professions_id = 0


class My_button:
    # создание кнопки
    def __init__(self, text, font, x, y, width, command):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.command = command

        self.button = Button(text=self.text, font=self.font, command=self.command)
        self.button.place(x=self.x, y=self.y, width=self.width)


class My_label:
    # создание текста
    def __init__(self, text, font, x, y, color):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.color = color

        self.label = Label(text=self.text, font=self.font, background=self.color)
        self.label.place(x=self.x, y=self.y)


class My_entry:
    # создание окошка для ввода данных
    def __init__(self, font, x, y, width):
        self.font = font
        self.x = x
        self.y = y
        self.width = width

        self.entry = Entry(font=self.font)
        self.entry.place(x=self.x, y=self.y, width=self.width)


class Window:
    # создание окна
    def __init__(self):
        self.canvas = None
        # создание окна
        self.window = Tk()
        # размеры окна
        self.width = 1500
        self.height = 900
        # цвет окна
        self.color = '#FFCF44'

        # задача размера окна
        self.window.geometry(f'{self.width}x{self.height}')
        # название окна
        self.window.title('Завод Санёк - качество не наш конёк')
        # запрет на расширение размеров окна
        self.window.resizable(height=False, width=False)

        # вызов функций
        self.create_canvas()
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.window.mainloop()

    def create_canvas(self):
        # создание холста
        self.canvas = Canvas(
            self.window,
            # размеры холста
            width=self.width,
            height=self.height,
            # цвет холста
            background=self.color)

        # формирование холста
        self.canvas.pack()

    def create_labels(self):
        # создание текста
        My_label('Введите логин: ', 'Arial200', 350, 300, color=self.color)
        My_label('Введите пароль: ', 'Arial200', 350, 350, color=self.color)

    def create_entries(self):
        # создание окошек для ввода данных
        self.login = My_entry(font='Arial 20', x=550, y=295, width=500)
        self.password = My_entry(font='Arial 20', x=550, y=345, width=500)

    def create_buttons(self):
        # создание кнопки
        My_button('Ввести', font='Arial 10', x=740, y=410, width=100, command=self.record_information)

    def record_information(self):
        global error_input
        global block
        error_window = 'Попробуйте снова через 5 минут после закрытия сообщения об этой ошибке.'
        # ввод данных в БД
        print('Кнопка нажата')
        self.hash_login = hashlib.md5(self.login.entry.get().encode())
        self.hash_password = hashlib.md5(self.password.entry.get().encode())

        self.login_value = self.hash_login.hexdigest()
        self.password_value = self.hash_password.hexdigest()

        # уведомление о вводе данных в БД

        if not self.check_all_entries_are_filled():
            showerror('Ошибка!', 'Не все данные заполнены!')
        else:
            if self.check_password():
                self.insert_data_in_database()
                showinfo('Операция прошла успешно', f'Добро пожаловать!')
                self.new_window()
            else:
                showerror('Ошибка!', 'Не верный логин или пароль!')
                error_input += 1
                if error_input == 3:
                    showerror('Ошибка!', f'Превышен лимит попыток ввода пароля! {error_window}')
                    time.sleep(300)
                    error_input = 0

    def new_window(self):
        self.window.quit()
        self.window.destroy()
        window2 = New_window()

    def check_password(self):
        new_password = self.get_password(self.login_value)

        if not new_password:
            return False
        else:
            if self.password_value == new_password:
                return True
            else:
                return False

    def check_all_entries_are_filled(self):
        if not self.password_value or not self.login_value:
            return False
        else:
            return True

    def get_password(self, login):
        connection = sqlite3.connect('professions_bd.db')
        cursor = connection.cursor()

        cursor.execute(f"SELECT password FROM people WHERE login = '{login}'")
        result=cursor.fetchone()
        cursor.close()
        connection.close()

        if not result:
            return ''
        else:
            return result[0]

    def insert_data_in_database(self):
        global user
        # заполнение БД данными пользователя
        # подключение к БД для заполнение её данными пользователя
        connection = sqlite3.connect('professions_bd.db')
        cursor = connection.cursor()

        cursor.execute(f"SELECT id FROM people WHERE login = '{self.login_value}'")
        result = cursor.fetchone()

        user = result[0]

        cursor.execute(f"INSERT INTO input (time, people) VALUES('{datetime.datetime.now()}', '{user}')")

        connection.commit()

        cursor.close()
        connection.close()


class New_window:
    def __init__(self):
        self.canvas = None
        # создание окна
        self.window2 = Tk()
        # размеры окна
        self.width = 1500
        self.height = 900
        # цвет окна
        self.color = '#FFCF44'

        # задача размера окна
        self.window2.geometry(f'{self.width}x{self.height}')
        # название окна
        self.window2.title('Завод Санёк - качество не наш конёк')
        # запрет на расширение размеров окна
        self.window2.resizable(height=False, width=False)

        # вызов функций
        self.create_canvas()
        self.create_labels()
        # self.create_entries()
        # self.create_buttons()
        self.window2.mainloop()

    def create_canvas(self):
        # создание холста
        self.canvas = Canvas(
            self.window2,
            # размеры холста
            width=self.width,
            height=self.height,
            # цвет холста
            background=self.color)

        # формирование холста
        self.canvas.pack()

    def create_labels(self):
        # создание текста
        My_label(self.get_user(), 'Arial200', 10, 10, color=self.color)
        My_label(self.get_user_professions(), 'Arial200', 10, 60, color=self.color)
        My_label('Работы пока нет', 'Arial200', 10, 110, color=self.color)
        if professions_id == 1:
            My_label('Список последних 10 входов в программу: ', 'Arial200', 500, 60, color=self.color)
            My_label('(время / ФИО)', 'Arial200', 500, 110, color=self.color)
            for i in self.get_login_history():
                My_label(i, 'Arial200', 500, y=((self.get_login_history().index(i)+1)*50)+110, color=self.color)

    def create_entries(self):
        # создание окошек для ввода данных
        self.login = My_entry(font='Arial 20', x=550, y=295, width=500)

    def create_buttons(self):
        # создание кнопки
        My_button('Ввести', font='Arial 10', x=740, y=410, width=100, command=self.record_information)

    def record_information(self):
        pass

    def get_login_history(self):
        connection = sqlite3.connect('professions_bd.db')
        cursor = connection.cursor()

        cursor.execute(f"select * from (SELECT row_number() OVER (ORDER BY i.time DESC) num, i.time, "
                       f"p.surname||' '||p.name||' '||p.patronymic name FROM input i JOIN people p ON p.id = i.people) "
                       f"as t WHERE num <= 10 order by num")
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result

    def get_user(self):
        global user
        connection = sqlite3.connect('professions_bd.db')
        cursor = connection.cursor()

        cursor.execute(f"SELECT surname FROM people WHERE id = {user}")
        result = cursor.fetchone()

        cursor.execute(f"SELECT name FROM people WHERE id = {user}")
        result2 = cursor.fetchone()

        cursor.execute(f"SELECT patronymic FROM people WHERE id = {user}")
        result3 = cursor.fetchone()

        cursor.close()
        connection.close()

        return 'Добро пожаловать: ' + str(result[0]) + ' ' + str(result2[0]) + ' ' + str(result3[0])

    def get_user_professions(self):
        global user
        global professions_id
        connection = sqlite3.connect('professions_bd.db')
        cursor = connection.cursor()

        cursor.execute(f"SELECT professions.professions, professions.id FROM workers LEFT JOIN professions "
                       f"ON workers.professions_id = professions.id WHERE people_id = '{user}'")

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        professions_id = result[1]

        return 'Ваша должность: ' + str(result[0])

    def insert_data_in_database(self):
        global user
        # заполнение БД данными пользователя
        # подключение к БД для заполнение её данными пользователя
        connection = sqlite3.connect('professions_bd.db')
        cursor = connection.cursor()

        connection.commit()

        cursor.close()
        connection.close()


# создание экземпляра класса окно
window = Window()
