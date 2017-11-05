#!/usr/bin/python
from tkinter import *
import os


class Mainwindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("400x300")
        self.recipe_lst = {
            'name': StringVar(),
            'time': StringVar(),
            'ingredient': StringVar(),
            'directions': StringVar()
        }

        menubar = Menu(self)
        self.config(menu=menubar)
        filemenu = Menu(menubar)
        # filemenu.add_command(label = 'Open', command = self.open)
        # menubar.add_cascade(label = 'File', menu = filemenu)

        self.text = Text(self)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (Page_One, Page_Two, Page_Three):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Page_One")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class Page_One(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.entry = Entry(self, textvariable=self.controller.recipe_lst['name'], width=25, bd=5)
        self.entry.grid(row=0, column=1)
        self.entry_t = Entry(self, textvariable=self.controller.recipe_lst['time'], width=25, bd=5)
        self.entry_t.grid(row=1, column=1)
        self.entry_i = Entry(self, textvariable=self.controller.recipe_lst['ingredient'], width=25, bd=5)
        self.entry_i.grid(row=2, column=1)
        self.entry_d = Entry(self, textvariable=self.controller.recipe_lst['directions'], width=25, bd=5)
        self.entry_d.grid(row=3, column=1)
        # self.entry_c = Entry(self, width=25, bd=5)
        # self.entry_c.grid(row=4, column=1)

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


        self.button = Button(self, text="View Recipe List",
                             command=lambda: [controller.show_frame("Page_Two"), self.print_names()])
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

    def save_recipe(self):
        if not os.path.exists(os.getcwd() + "\Recipes"):
            os.makedirs(os.getcwd() + "\Recipes")
        recipe_path = (os.getcwd() + "\Recipes")

        if not os.getcwd() == recipe_path:
            os.chdir("Recipes")

        f_name = self.entry.get()
        t_name = self.entry_t.get()
        i_name = self.entry_i.get()
        d_name = self.entry_d.get()

        with open(f_name + ".txt", "w") as f:
            f.write(f_name)
            f.write(os.linesep)
            f.write(t_name)
            f.write(os.linesep)
            f.write(i_name)
            f.write(os.linesep)
            f.write(d_name)
            f.close()


class Page_Two(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.label = Label(self, text="Recipe Page")
        self.label.grid(row=0, column=0)

        self.button3 = Button(self, text="Return Home", command=lambda: controller.show_frame("Page_One"))
        self.button3.grid(row=0, column=1)
        # self.button4 = Button(self, text = "View Recipe Names", command = self.print_names)
        # self.button4.grid(row = 1, column = 2)
        self.button5 = Button(self, text="Load Recipe",
                              command=lambda: [controller.show_frame("Page_Three"), self.load_recipe()])
        self.button5.grid(row=2, column=2)

        self.listbox = Listbox(self)
        self.listbox.grid(row=2, column=0, columnspan=2)

    def load_recipe(self):
        selected = listbox.get('active')

        if selected == f_name:
            with open('f_name.txt', 'r') as f:
                f.read(f_name)


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
