from models import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.tix import *
import cloud_dump
import csv
import pandas as pd
from PIL import Image, ImageTk

class GUIHandler:
 
    def __init__(self):
        self.__db = db
        self.current_table = None # Хранит текущую таблицу

        # Начальное окно
        self.root = tk.Tk()
        self.root.title('Авторизация')
        self.root.geometry('400x150')
        
        ico = Image.open('ico.png')
        photo = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, photo)

        # Выбор действий
        self.menu_frame = tk.Frame(self.root, height= 15)
        tk.Button(self.menu_frame, cursor="hand2", text="Авторизоватья", font=('Calibri', 10), width= 15,
        command=lambda: self.user_authorization()).pack(side=tk.LEFT, fill='x', padx=1, pady=1, anchor = 'nw', expand=True)
        tk.Button(self.menu_frame, cursor="hand2", text="Зарегестрироваться", font=('Calibri', 10), width= 15,
        command=lambda: self.user_registration()).pack(side=tk.LEFT, fill='x', padx=1, pady=1, anchor = 'nw', expand=True)
        self.menu_frame.pack(expand=True, fill=tk.BOTH, anchor = 'n')

        # Окно ввода
        self.input_frame = tk.Frame(self.root, borderwidth=3)
        self.input_frame.pack(side=tk.TOP, fill=tk.X)
        self.user = tk.Entry(self.input_frame)
        self.password = tk.Entry(self.input_frame, show="*")
        
        tk.Label(self.input_frame, text='Имя').pack(side=tk.TOP, padx=1, pady=3, anchor = 'w', expand=True)
        self.user.pack(side=tk.TOP, padx=1, pady=3, anchor = 'w', expand=True)
        tk.Label(self.input_frame, text='Пороль').pack(side=tk.TOP, padx=1, pady=3, anchor = 'w', expand=True)
        self.password.pack(side=tk.TOP, padx=1, pady=3, anchor = 'w', expand=True)

    def user_registration(self):
        try:
            Account.create(
            name = self.user.get(),
            password = self.password.get()
            )
            messagebox.showerror("Регистрация", "Вы удачно зарегестрировались")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка выполнения запроса: {e}")

    def user_authorization(self):
        try:
            query = Account.select().where(Account.name == self.user.get()).where(Account.password == self.password.get())
            if query.exists():
                user = self.user.get()
                self.root.destroy()
                self.show_main_window(user)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка выполнения запроса: {e}")

    def add_null(self, id):
        Product.create(
                    compilation_id = id,
                    type = "Null",
                    name = "Null",
                    author = "Null",
                    genre = ["Null"],
                    release_date = "2000-01-01",
                    description = "Null", 
                    personal_rating = 0,
                    aggregator_rating = 0,
                    personal_review = "Null")
        self.get_comp(id, Product.select().where(Product.compilation_id == id))

    def show_field(self, id, id_pr, field):
        window = tk.Toplevel(self.root)
        window.title("Содержаине")
        window.geometry('300x280')

        pr = Product.get(Product.id == id_pr)
        if field == "Тип":
            start_text = pr.type
        elif field == "Имя":
            start_text = pr.name
        elif field == "Автор":
            start_text = pr.author
        elif field == "Жанры":
            start_arr = pr.genre
            start_text = ""
            for el in start_arr:
                start_text += el[0]
        elif field == "Релиз":
            start_text = pr.release_date
        elif field == "Описание":
            start_text = pr.description
        elif field == "Рейтинг":
            start_text = pr.personal_rating
        elif field == "Рейтинг аггрегаторов":
            start_text = pr.aggregator_rating
        elif field == "Обзор":
            start_text = pr.personal_review
        

        textF = tk.Text(window, font=('Calibri', 10), height=15)
        textF.insert("1.0", start_text)
        textF.pack()

        def change():
            try:
                text = textF.get("1.0", "end")
                text = text.replace("\n", " ")
                text = text[:len(text)-1]

                if field == "Тип":
                    Product.update(type = text).where(Product.id == id_pr).execute()
                elif field == "Имя":
                    Product.update(name = text).where(Product.id == id_pr).execute()
                elif field == "Автор":
                    Product.update(author = text).where(Product.id == id_pr).execute()
                elif field == "Жанры":
                    arr_text = text.split(", ")
                    Product.update(genre = arr_text).where(Product.id == id_pr).execute()
                elif field == "Релиз":
                    Product.update(release_date = text).where(Product.id == id_pr).execute()
                elif field == "Описание":
                    Product.update(description = text).where(Product.id == id_pr).execute()
                elif field == "Рейтинг":
                    Product.update(personal_rating = text).where(Product.id == id_pr).execute()
                elif field == "Рейтинг аггрегаторов":
                    Product.update(aggregator_rating = text).where(Product.id == id_pr).execute()
                elif field == "Обзор":
                    Product.update(personal_review = text).where(Product.id == id_pr).execute()
                window.destroy()
                self.get_comp(id, res = Product.select().where(Product.compilation_id == id))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка выполнения запроса: {e}")
        
        tk.Button(window, text="Изменить", command = lambda: change()).pack(pady=10)

    def delete_product(self, comp_id, id):
        try:
            row = Product.get(Product.id == id)
            row.delete_instance()

            self.get_comp(comp_id, Product.select().where(Product.compilation_id == comp_id))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения записи: {e}")

    def get_comp(self, id, res):
        for widget in self.frame.winfo_children():
            widget.destroy()

        def do_popup(event, menu): 
                    try: 
                        menu.tk_popup(event.x_root, event.y_root) 
                    finally: 
                        menu.grab_release() 

        row = 2
        for pr in res:
            button = tk.Button(self.frame, text=pr.type, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda id_pr = pr.id: self.show_field(id, id_pr, "Тип"))
            button.grid(row = row, column = 0)
            m = tk.Menu(button, tearoff = 0) 
            m.add_command(label ="Удалить", command = lambda comp=id, pr=pr.id: self.delete_product(comp, pr))
            button.bind("<Button-3>", func=lambda event, m=m: do_popup(event, m)) 

            tk.Button(self.frame, text=pr.name, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda id_pr = pr.id: self.show_field(id, id_pr, "Имя")).grid(row = row, column = 1)
            tk.Button(self.frame, text=pr.author, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda id_pr = pr.id: self.show_field(id, id_pr, "Автор")).grid(row = row, column = 2)
            
            genres = ""
            if pr.genre:
                for el in pr.genre:
                    genres += el + ", "
                genres = genres[:len(genres)-2]

            tk.Button(self.frame, text=genres, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda id_pr = pr.id: self.show_field(id, id_pr, "Жанры")).grid(row = row, column = 3)
            tk.Button(self.frame, text=pr.release_date, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda id_pr = pr.id: self.show_field(id, id_pr, "Релиз")).grid(row = row, column = 4)
            tk.Button(self.frame, text=pr.description, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda id_pr = pr.id: self.show_field(id, id_pr, "Описание")).grid(row = row, column = 5)
            tk.Button(self.frame, text=pr.personal_rating, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda id_pr = pr.id: self.show_field(id, id_pr, "Рейтинг")).grid(row = row, column = 6)
            tk.Button(self.frame, text=pr.aggregator_rating, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda id_pr = pr.id: self.show_field(id, id_pr, "Рейтинг аггрегаторов")).grid(row = row, column = 7)
            tk.Button(self.frame, text=pr.personal_review, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda id_pr = pr.id: self.show_field(id, id_pr, "Обзор")).grid(row = row, column = 8)
            row+=1
        tk.Button(self.frame, text="ДОБАВИТЬ СТРОКУ", font=('Calibri', 10), width= 20, bd = 0,
            command=lambda: self.add_null(id)).grid(row = row, column = 0)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_comp(self, user):
        window = tk.Toplevel(self.root)
        window.title("Настройки подборки")
        window.geometry('200x200')
        
        fields = ['Название', 'Описание']
        entries = {}
        for field in fields:
            frame = tk.Frame(window)
            frame.pack(fill=tk.X, pady=5)
            tk.Label(frame, text=field, width=15, anchor='w').pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entries[field] = entry
            entry.pack(fill=tk.X, padx=5, expand=True)

    
        def submit():
            data = {field: entry.get() for field, entry in entries.items()}
            
            try:
                Compilation.create(
                    name = data['Название'],
                    description = data['Описание'],
                    account_id = user)
                
                self.root.destroy()
                self.show_main_window(user) # Обновляем таблицу
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения записи: {e}")
        tk.Button(window, text="Сохранить", command=submit).pack(pady=10)

    def delete_comp(self, user, name):
        try:
            row = Compilation.get(Compilation.name == name, 
                                    Compilation.account_id == user)
            row.delete_instance()

            self.root.destroy()
            self.show_main_window(user) # Обновляем таблицу
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения записи: {e}")

    def dump_comp(self, id, file_name):
        try:
           file_name += ".csv"
           with open(file_name, 'w') as fh:
            query = (Product.select(Product.type, Product.name, Product.author, Product.genre, Product.release_date, 
                                    Product.description, Product.personal_rating, Product.aggregator_rating, Product.personal_review)
                     .where(Product.compilation_id == id)
                     .tuples())
            writer = csv.writer(fh)
            for row in query:
                writer.writerow(row)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения записи: {e}")

    def dump_on_drive(self, id, file_name):
        try:
           file_name += ".csv"
           with open(file_name, 'w') as fh:
            query = (Product.select(Product.type, Product.name, Product.author, Product.genre, Product.release_date, 
                                    Product.description, Product.personal_rating, Product.aggregator_rating, Product.personal_review)
                     .where(Product.compilation_id == id)
                     .tuples())
            writer = csv.writer(fh)
            for row in query:
                writer.writerow(row)
            cloud_dump.on_drive(file_name)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения записи: {e}")
    
    def dump_xlsx(self, id):
        try:
           comp_query = Compilation.select().where(Compilation.account_id == id)
           file_name = Account.get(Account.id == id).name + ".xlsx"
           datatoexcel = pd.ExcelWriter(file_name)
           for comp in comp_query:
                pr_query = Product.select().where(Product.compilation_id == comp.id)
                type_list = []
                name_list = []
                aut_list = []
                gen_list = []
                rel_list = []
                dis_list = []
                r_list = []
                ra_list = []
                rew_list = []
                for pr in pr_query:
                    a= pr.genre
                    type_list.append(pr.type)
                    name_list.append(pr.name)
                    aut_list.append(pr.author)
                    gen_list.append(pr.genre)
                    rel_list.append(pr.release_date)
                    dis_list.append(pr.description)
                    r_list.append(pr.personal_rating)
                    ra_list.append(pr.aggregator_rating)
                    rew_list.append(pr.personal_review)

                data = {"Тип" : type_list, "Название" : name_list, "Автор" : aut_list, "Жанры" : gen_list, "Дата выхода" : rel_list,
                         "Описание" : dis_list, "Рейтинг" : r_list, "Рейтинг аггрегаторов" : ra_list, "Обзор" : rew_list}
                df = pd.DataFrame(data)
                df.to_excel(datatoexcel, sheet_name=comp.name, index = False)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения записи: {e}")
        datatoexcel.close()

    def show_content(self, content):
        window = tk.Toplevel(self.root)
        window.title("Содержаине")
        window.geometry('300x300')

        text = tk.Text(window, font=('Calibri', 10))
        text.pack()
        text.insert("1.0", content)

    def show_main_window(self, user):
        self.root = tk.Tk()
        self.root.title('Авторизация')
        self.root.geometry('1300x600')
        self.root.resizable(False, False)

        ico = Image.open('ico.png')
        photo = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, photo)

        main_menu = tk.Menu()
        main_menu.add_cascade(label="Добавить", command=lambda: self.create_comp(user))
        main_menu.add_cascade(label="Сформировать xlsx", command=lambda: self.dump_xlsx(user))
        self.root.config(menu=main_menu)


        compF = tk.Frame(self.root)
        res = Compilation.select(Compilation.name, Compilation.id, Compilation.description)
        tk.Label(compF, text="Выберите подборку:", font=('Calibri', 10), anchor='w').pack(side = 'left', anchor='w')
        r = 2
        
        def do_popup(event, menu): 
                    try: 
                        menu.tk_popup(event.x_root, event.y_root) 
                    finally: 
                        menu.grab_release() 
        for add in res:
            button = tk.Button(compF, cursor="hand2", text=add.name, font=('Calibri', 16), width= len(add.name)+1, bd = 1,
            command=lambda id=add.id: self.get_comp(id, Product.select().where(Product.compilation_id == id)))
            button.pack(anchor='w', side = 'left', padx = 2)
            m = tk.Menu(button, tearoff = 0) 
            m.add_command(label ="Описание", command = lambda d=add.description: self.show_content(d))
            m.add_command(label ="Удалить", command = lambda n=add.name: self.delete_comp(user, n))
            m.add_command(label ="Выгрузить в CSV", command = lambda id=add.id, name = add.name: self.dump_comp(id, name))
            m.add_command(label ="Выгрузить CSV на Google Drive", command = lambda id=add.id, name = add.name: self.dump_on_drive(id, name))
            button.bind("<Button-3>", func=lambda event, m=m: do_popup(event, m)) 

            r += 1

        compF.pack(side = 'top', anchor='w')

        header = tk.Frame(self.root)
        c = 0
        for head in ["Тип", "Название", "Автор", "Жанры", "Дата выпуска", "Описание", "Личный рейтинг", "Рейтинг аггрегаторов", "Обзор"]:
            tk.Button(header, text=head, font=('Calibri', 10), width= 20, bd = 0, anchor='w',
            command=lambda: self.user_authorization()).grid(row = 1, column = c)
            c += 1
        header.pack(anchor='center')

        
        self.canvas = tk.Canvas(self.root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        
    def run(self):
        self.root.mainloop()