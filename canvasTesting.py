from tkinter import *
from tkinter import ttk


canvasOn = True

def toggleCanvas(*args):

    print(args)

    global canvasOn, canvas

    if canvasOn:
        canvas.grid_remove()
        canvasOn = False
    else:
        canvas.grid()
        canvasOn = True

def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))



def createCheckButtons(master):

    for i in range (1,20):
        tempCheck = Checkbutton(master, text="This is button {}".format(i))
        tempCheck.grid(column=5, row=i)

root = Tk()


menuItem = ["Click me!"]
menuItem = StringVar(value=menuItem)

box = Listbox(root, listvariable=menuItem)
box.grid(column=0, row=0)


# Now the canvas and its contents
canvas = Canvas(root)
canvas.grid(column=1, row=0)


frame = Frame(canvas)
canvas.create_window((4,4), window=frame)
createCheckButtons(frame)

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

box.bind("<Double-1>", toggleCanvas)
root.mainloop()




