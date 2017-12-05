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
            'directions': StringVar()
        }

    def create_container(self):
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        return container

    def create_pages(self, container):
        for F in (Page_One, Page_Two, Page_Three):
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
        self.entry = Entry(self, textvariable=self.controller.recipe_dict['name'], width=25, bd=5)
        self.entry.grid(row=0, column=1)
        self.entry_t = Entry(self, textvariable=self.controller.recipe_dict['time'], width=25, bd=5)
        self.entry_t.grid(row=1, column=1)
        self.entry_i = Entry(self, textvariable=self.controller.recipe_dict['ingredient'], width=25, bd=5)
        self.entry_i.grid(row=2, column=1)
        self.entry_d = Entry(self, textvariable=self.controller.recipe_dict['directions'], width=25, bd=5)
        self.entry_d.grid(row=3, column=1)
        # self.entry_c = Entry(self, width=25, bd=5)
        # self.entry_c.grid(row=4, column=1)

    def create_entry_labels(self):
        self.lbl = Label(self, text="Name", bg="teal", fg="white")
        self.lbl.grid(row=0, column=0)
        self.lbt = Label(self, text="Total Time", bg="teal", fg="white")
        self.lbt.grid(row=1, column=0)
        self.lbi = Label(self, text="Ingredients", bg="teal", fg="white")
        self.lbi.grid(row=2, column=0)
        self.lbd = Label(self, text="Directions", bg="teal", fg="white")
        self.lbd.grid(row=3, column=0)
        # self.lbc = Label(self, text="Category", bg="teal", fg="white")
        # self.lbc.grid(row=4, column=0)

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
        self.entry_d.delete(0, "end")
        self.entry.focus()

    def print_names(self):
        name = self.entry.get()
        self.controller.listbox("end", name)

    def create_py_dict(self):
        f_name = self.entry.get()
        t_name = self.entry_t.get()
        i_name = self.entry_i.get()
        d_name = self.entry_d.get()

        self.recipe_list = [f_name, t_name, i_name, d_name]
        self.save_pydict = self.controller.recipe_dict

        for key in self.save_pydict:
            count = 0
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

        with open(json_file_name + ".json", "w") as f:
            json.dump(self.save_pydict, f)


class Page_Two(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.label = Label(self, text="Recipe Page")
        self.label.grid(row=0, column=0)

        self.button3 = Button(self, text="Return Home", command=lambda: controller.show_frame("Page_One"))
        self.button3.grid(row=0, column=2)
        # self.button4 = Button(self, text = "View Recipe Names", command = self.print_names)
        # self.button4.grid(row = 1, column = 2)
        self.button5 = Button(self, text="Load Recipe",
                              command=lambda: [controller.show_frame("Page_Three"), self.load_recipe()])
        self.button5.grid(row=2, column=2)
        self.button5 = Button(self, text="Refresh List",
                              command=lambda: [controller.show_frame("Page_Two"), self.display_saved_recipes()])
        self.button5.grid(row=1, column=2)

        self.listbox = Listbox(self)
        self.listbox.grid(row=2, column=0, columnspan=2)

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
        selected = self.listbox.get('active')


class Page_Three(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.button6 = Button(self, text="Go Back", command=lambda: controller.show_frame("Page_Two"))
        self.button6.grid(row=0, column=0)


if __name__ == "__main__":
    app = Mainwindow()
    app.title('Recipe Book')
    app.mainloop()
