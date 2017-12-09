#!/usr/bin/python
from tkinter import *
import os
import json


class Mainwindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.cwd = os.getcwd()
        self.geometry("400x300")
        self.create_list_fields()
        self.create_menu_bar()
        self.text = Text(self)
        container = self.create_container()
        self.create_pages(container)
        self.show_frame("Page_One")

    def create_menu_bar(self):
        menubar = Menu(self)
        self.config(menu=menubar)
        filemenu = Menu(menubar)
        # filemenu.add_command(label = 'Open', command = self.open)
        # menubar.add_cascade(label = 'File', menu = filemenu)

    def create_list_fields(self):
        self.recipe_dict = {
            'name': StringVar(),
            'time': StringVar(),
            'ingredient': StringVar(),
            'category' : StringVar(),
            'directions': StringVar()
        }

        self.option_list = ['', 'breakfast', 'lunch', 'dinner']

    def create_container(self):
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        return container

    def create_pages(self, container):
        for F in (Page_One, Page_Two):
            # add attribute __name__
            page_name = F.__name__
            # create an object
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Page_One(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.create_entry_fields()
        self.create_entry_labels()
        self.create_buttons()

    def create_entry_fields(self):
        self.entry = Entry(self, width=25, bd=3)
        self.entry.grid(row=0, column=1, pady=5)
        self.entry_t = Entry(self, width=25, bd=3)
        self.entry_t.grid(row=1, column=1, pady=5)
        self.entry_i = Entry(self, width=25, bd=3)
        self.entry_i.grid(row=2, column=1, pady=5)
        self.entry_ol = StringVar()
        self.entry_ol.set(self.controller.option_list[0])
        self.entry_c = OptionMenu(self, self.entry_ol, *self.controller.option_list, command=self.optmenuupdate)
        self.entry_c.grid(row=3, column=1)
        self.entry_d = Text(self, height=10, width=19, bd=3)
        self.entry_d.grid(row=4, column=1)


    def create_entry_labels(self):
        self.lbl = Label(self, text="Name", fg="black")
        self.lbl.grid(row=0, column=0)
        self.lbt = Label(self, text="Total Time", fg="black")
        self.lbt.grid(row=1, column=0)
        self.lbi = Label(self, text="Ingredients", fg="black")
        self.lbi.grid(row=2, column=0)
        self.lbc = Label(self, text="Category", fg="white")
        self.lbc.grid(row=3, column=0)
        self.lbd = Label(self, text="Directions", fg="black")
        self.lbd.grid(row=4, column=0)


    def create_buttons(self):
        self.button = Button(self, text="View Recipe List",
                             command=lambda: [self.controller.show_frame("Page_Two")])
        self.button.grid(row=1, column=2)
        self.button2 = Button(self, text="Save Recipe", command=lambda: [self.save_recipe(), self.clear_entries()])
        self.button2.grid(row=2, column=2)

    def clear_entries(self):
        self.entry.delete(0, "end")
        self.entry_t.delete(0, "end")
        self.entry_i.delete(0, "end")
        self.entry_ol.set(self.controller.option_list[0])
        self.entry_d.delete(1.0, END)

        self.entry.focus()

    def print_names(self):
        name = self.entry.get()
        self.controller.listbox("end", name)

    def optmenuupdate(self, value):
        for i in self.controller.option_list:
            if value == i:
                self.c_name = i

    def create_py_dict(self):
        f_name = self.entry.get()
        t_name = self.entry_t.get()
        i_name = self.entry_i.get()
        c_name = self.c_name
        d_name = self.entry_d.get("1.0", END)

        self.recipe_list = [f_name, t_name, i_name, c_name, d_name]
        self.save_pydict = self.controller.recipe_dict

        count = 0
        for key in self.save_pydict:
            self.save_pydict[key] = self.recipe_list[count]
            count+=1

        return f_name

    def save_recipe(self):
        if not os.path.exists(os.path.join(self.controller.cwd, "Recipes")):
            os.makedirs(os.path.join(self.controller.cwd, "Recipes"))
        recipe_path = (os.path.join(self.controller.cwd, "Recipes"))

        if os.getcwd() != recipe_path:
            os.chdir(recipe_path)

        json_file_name = self.create_py_dict()

        if len(json_file_name) > 0:
            with open(json_file_name + ".json", "w") as f:
                json.dump(self.save_pydict, f)


class Page_Two(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.label = Label(self, text="Recipe Page")
        self.label.grid(row=0, column=0)

        self.button3 = Button(self, text="Return Home", command=lambda: controller.show_frame("Page_One"))
        self.button3.grid(row=1, column=0)

        self.button4 = Button(self, text="Load Recipe",command=lambda:[controller.show_frame("Page_Two"), self.load_recipe()])
        self.button4.grid(row=0, column = 1)

        self.button5 = Button(self, text="Refresh List",
                              command=lambda: [controller.show_frame("Page_Two"), self.display_saved_recipes()])
        self.button5.grid(row=1, column=1)

        self.listbox = Listbox(self)
        self.listbox.grid(row=2, column=0, columnspan=2)

        self.listbox2 = Listbox(self)
        self.listbox2.grid(row = 2, column = 2, columnspan = 2)

        self.display_saved_recipes()

    def display_saved_recipes(self):
        self.listbox.delete(0, END)
        if not os.path.exists(os.path.join(self.controller.cwd, "Recipes")):
            os.makedirs(os.path.join(self.controller.cwd, "Recipes"))
        count = 0
        for filename in os.listdir((os.path.join(self.controller.cwd, "Recipes"))):
            self.listbox.insert(count, os.path.splitext(filename)[0])
            count+=1

    def load_recipe(self):
        self.listbox2.delete(0,END)
        selected = self.listbox.get('active')
        json_file = os.path.join(self.controller.cwd, "Recipes", selected) + ".json"
        with open(json_file, "r") as f:
            data = f.read()

        json_recipe = json.loads(data)

        for item in json_recipe:
            self.listbox2.insert(END,'{}: {}'.format(item, json_recipe.get(item)))


if __name__ == "__main__":
    app = Mainwindow()
    app.title('Recipe Book')
    app.mainloop()
