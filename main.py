
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showinfo, askyesno
from tkinter.ttk import Combobox

COLORFON = '#2E8B57'
COLORBUT = '#006400'
COLORTEXT = '#FFFFFF'
# Класс для работы с бд
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("mybooks.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS buy (id INTEGER PRIMARY KEY, product TEXT, price TEXT, comment TEXT, kategory TEXT)")
        self.conn.commit()



    def __del__(self):
        self.conn.close()

    #Записи о покупках
    def view(self):
        self.cur.execute("SELECT * FROM buy")
        rows = self.cur.fetchall()
        return rows

    #Записи о сумме трат
    def view_sum(self):
        self.cur.execute("SELECT SUM(price) FROM buy")
        rows = self.cur.fetchall()
        return rows

    # добавление новой записи
    def insert(self, product, price, comment, kategory):
        self.cur.execute("INSERT INTO buy VALUES (NULL,?,?,?,?)", (product, price, comment, kategory))
        self.conn.commit()

    # обновляем информации о покупки
    def update(self, id, product, price):
        self.cur.execute("UPDATE buy SET product=?, price=? WHERE id=?", (product, price, id,))
        self.conn.commit()

    # удаление  записи
    def delete(self, id):
        self.cur.execute("DELETE FROM buy WHERE id=?", (id,))
        self.conn.commit()

    # Поиск по названию продукта
    def search(self, product, ):
        self.cur.execute("SELECT * FROM buy WHERE product = ?", (product,))
        rows = self.cur.fetchall()
        return rows

# Поиск по Категории
    def search_kategory(self, kategory, ):
        self.cur.execute("SELECT * FROM buy WHERE kategory = ?", (kategory,))
        rows = self.cur.fetchall()
        return rows

db = DB()


def get_selected_row(event):
    global selected_tuple
    index = list1.curselection()[0]
    selected_tuple = list1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[1])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3])
    e4.delete(0, END)
    e4.insert(END, selected_tuple[4])


# обработчик нажатия на кнопку «Посмотреть всё»
def view_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)

# обработчик нажатия на кнопку «Поиск»
def search_command():
    list1.delete(0, END)
    for row in db.search(product_search.get()):
        list1.insert(END, row)

# обработчик нажатия на кнопку «Поиск по категории»
def search_kategory_command():
    list1.delete(0, END)
    for row in db.search_kategory(kategory_search.get()):
        list1.insert(END, row)
#
def view_sum_command():
    list2.delete(0, END)
    for row in db.view_sum():
        list2.insert(END, row)
# обработчик нажатия на кнопку «Добавить»
def add_command():
    result = askyesno(title="Подтвержение добавления", message="Подтвердить добавления?")
    if result:
        db.insert(product_text.get(), price_text.get(), comment_text.get(), kategory_text.get())
        view_command()
        showinfo("Результат", "Добавлено")
    else:
        showinfo("Результат", "отменена")


# обработчик нажатия на кнопку «Удалить»
def delete_command():
    result = askyesno(title="Подтвержение удаления", message="Подтвердить удаление?")
    if result:
        db.delete(selected_tuple[0])
        view_command()
        showinfo("Результат", "удалено")
    else:
        showinfo("Результат", "отменена")


# обработчик нажатия на кнопку «Обновить»
def update_command():
    result = askyesno(title="Подтвержение изменения", message="Подтвердить изменения?")
    if result:
        db.update(selected_tuple[0], product_text.get(), price_text.get())
        view_command()
        showinfo("Результат", "измененино")
    else:
        showinfo("Результат", "отменена")



window = Tk()
window.title("Слежка за расходами 0.1")
window.config(bg=COLORFON)


def on_closing():
    if messagebox.askokcancel("", "Закрыть программу?"):
        window.destroy()



window.protocol("WM_DELETE_WINDOW", on_closing)


l1 = Label(window, text="Название", bg=COLORFON, fg=COLORTEXT)
l1.grid(row=2, column=2, sticky=S)

l2 = Label(window, text="Стоимость", bg=COLORFON, fg=COLORTEXT)
l2.grid(row=2, column=3, sticky=S)

l3 = Label(window, text="Комментарий", bg=COLORFON, fg=COLORTEXT)
l3.grid(row=4, column=2, sticky=S)

l4 = Label(window, text="Категория", bg=COLORFON, fg=COLORTEXT)
l4.grid(row=4, column=3, sticky=S)

product_text = StringVar()
e1 = Entry(window, textvariable=product_text, bg=COLORBUT, fg=COLORTEXT)
e1.grid(row=3, column=2, sticky=N)

price_text = StringVar()
e2 = Entry(window, textvariable=price_text, bg=COLORBUT, fg=COLORTEXT)
e2.grid(row=3, column=3, sticky=N)

comment_text = StringVar()
e3 = Entry(window, textvariable=comment_text, bg=COLORBUT, fg=COLORTEXT)
e3.grid(row=5, column=2, sticky=N)

kadegoris = ["Продукты", "Медицина", "Развлечение", "Бытовые товары", "Техника", "Канцелярия"]
kategory_text = StringVar()
e4 = Combobox(window,textvariable= kategory_text, values=kadegoris)
e4.grid(row=5, column=3, sticky=N)

# поисковики
product_search = StringVar()
entry = Entry(window,bg=COLORBUT, fg=COLORTEXT, textvariable=product_search)
entry.grid(row=1, column=1, padx=5, pady=7, sticky=NSEW)

kategory_search = StringVar()
entry1 = Combobox(window,textvariable= kategory_search, values=kadegoris)
entry1.grid(row=1, column=3, padx=5, pady=7, sticky=NSEW)

# Вывод Всего
list1 = Listbox(window, height=25, width=65, bg=COLORBUT, fg=COLORTEXT)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)

list1.bind('<<ListboxSelect>>', get_selected_row)

list2 = Listbox(window, height=1, width=10, bg=COLORBUT, fg=COLORTEXT)
list2.grid(row=6, column=3, sticky=NSEW)

b1 = Button(window, text="Посмотреть все", width=12, command=view_command, bg=COLORBUT, fg=COLORTEXT)
b1.grid(row=1, column=0, padx=5, pady=7, sticky=NSEW)

b2 = Button(window, text="Поиск", width=12, command=search_command, bg=COLORBUT, fg=COLORTEXT)
b2.grid(row=1, column=2, padx=5, pady=7, sticky=NSEW)

b3 = Button(window, text="Добавить", width=12, command=add_command, bg=COLORBUT, fg=COLORTEXT)
b3.grid(row=2, column=4, sticky=NSEW)

b4 = Button(window, text="Обновить", width=12, command=update_command, bg=COLORBUT, fg=COLORTEXT)
b4.grid(row=3, column=4, sticky=NSEW)

b5 = Button(window, text="Удалить", width=12, command=delete_command, bg=COLORBUT, fg=COLORTEXT)
b5.grid(row=4, column=4, sticky=NSEW)

b6 = Button(window, text="Закрыть", width=12, command=on_closing, bg=COLORBUT, fg=COLORTEXT)
b6.grid(row=5, column=4, sticky=NSEW)

b7 = Button(window, text="Поиск по категории", width=12, command=search_kategory_command, bg=COLORBUT, fg=COLORTEXT)
b7.grid(row=1, column=4, padx=5, pady=7,ipadx=10, sticky=NSEW)

b8 = Button(window, text="Траты", width=12, command=view_sum_command, bg=COLORBUT, fg=COLORTEXT)
b8.grid(row=6, column=4, sticky=NSEW)

view_command()


window.mainloop()