from tkinter import *
from tkinter import ttk


def toggle(*args):

    global secondOn
    if secondOn:
        secondBox.grid_remove()
        secondOn = False
    else:
        secondOn = True
        secondBox.grid()



root = Tk()

programGroups = ["Automotive", "Web Development", "Welding", "CADD"]
boxValues = StringVar(value=programGroups)

mainBox = Listbox(root, listvariable=boxValues, height=6)
mainBox.grid(column=0, row=0)
mainBox.bind("<Double-1>", toggle)
programs = ["HiTECC AAT", "HiTECC CP", "Weld CP", "Welding AAT"]

secondBoxValues = StringVar(value=programs)

secondBox = Listbox(root, listvariable=secondBoxValues, height=6)
secondBox.grid(column=1, row=0)

secondOn = True


root.mainloop()