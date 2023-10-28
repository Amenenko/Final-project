import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс главного окна.
class EmployeeList(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = EmployeeDB()
        self.view_records()

    # Хранение и инициализация объектов GUI.
    def init_main(self):
        # Панель инструментов.
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления сотрудника.
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.add_img,
                                    command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # Кнопка изменения данных о сотруднике.
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.update_img,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Кнопка удаления сотрудника.
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.delete_img,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # Кнопка поиска сотрудника.
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления.
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                image=self.refresh_img,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Создание Treeview.
        self.tree = ttk.Treeview(self,
                                 columns=('ID', 'name', 'tel',
                                          'email', 'salary'),
                                 height=45, show='headings')
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=100, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='E-mail')
        self.tree.heading("salary", text='Зарплата')

        self.tree.pack(side=tk.LEFT)

        # Скроллбар для вертикальной прокрутки.
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Добавление записи.
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # Редактирование данных записи.
    def update_record(self, name, tel, email, salary):
        self.db.c.execute('''UPDATE employees SET name=?, tel=?,
                          email=?, salary=? WHERE ID=?''',
                          (name, tel, email, salary,
                           self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Вывод данных в виджет таблицы.
    def view_records(self):
        self.db.c.execute('''SELECT * FROM employees''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in
         self.db.c.fetchall()]

    # Удаление записи.
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM employees WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Поиск записи.
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM employees WHERE name LIKE ?''', name
                          )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall(
        )]

    # Вызов окна для добавления записи.
    def open_dialog(self):
        AddEmployee()

    # Вызов окна для редактирования данных записи.
    def open_update_dialog(self):
        UpdateEmployee()

    # Вызов окна для поиска записи.
    def open_search_dialog(self):
        SearchEmployee()


# Класс окна добавления записи.
class AddEmployee(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        # Настройки для дочернего окна.
        self.title('Добавить сотрудника')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # Подписи.
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)

        # Строка для ввода наименования.
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        # Строка для ввода email.
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        # Строка для ввода телефона.
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        # Строка для ввода заработной платы.
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        # Кнопка закрытия дочернего окна.
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy
                                     )
        self.btn_cancel.place(x=300, y=170)

        # Кнопка добавления.
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_email.get(),
                                           self.entry_tel.get(),
                                           self.entry_salary.get()))


# Класс окна для редактирования данных записи.
class UpdateEmployee(AddEmployee):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    # Инициализация окна для редактирования сотрудника.
    def init_edit(self):
        self.title('Редактировать сотрудника')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_email.get(),
                                              self.entry_tel.get(),
                                              self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    # Заполнение полей данными для редактирования сотрудника.
    def default_data(self):
        self.db.c.execute('''SELECT * FROM employees WHERE id=?''',
                          (self.view.tree.set(
                              self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


# Класс окна для поиска записи.
class SearchEmployee(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # Инициализация окна для поиска сотрудника.
    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(
                        self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


# Класс БД.
class EmployeeDB:
    def __init__(self):
        self.conn = sqlite3.connect('employees.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS employees
                          (id integer primary key, name text,
                           tel text, email text, salary real)''')
        self.conn.commit()

    # Добавление в БД.
    def insert_data(self, name, tel, email, salary):
        self.c.execute('''INSERT INTO employees (name, tel, email, salary)
                       VALUES (?, ?, ?, ?)''',
                       (name, tel, email, salary))
        self.conn.commit()


if __name__ == '__main__':
    # Создание основного окна.
    root = tk.Tk()
    db = EmployeeDB()
    app = EmployeeList(root)
    app.pack()

    # Настройки главного окна.
    root.title('Список сотрудников компании')
    root.geometry('800x600')
    root.resizable(False, False)

    # Запуск главного цикла приложения.
    root.mainloop()
