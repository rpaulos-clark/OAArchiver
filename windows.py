from tkinter import *
from tkinter import ttk


# def calculate(*args):
#     try:
#         value = float(feet.get())
#         meters.set((0.3048 * value * 10000.0 + .05)/10000.0)
#     except ValueError:
#         pass
#
#
# root = Tk()
# root.title("Feet to Meters")
# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# mainframe.columnconfigure(0, weight=1)
# mainframe.rowconfigure(0, weight=1)
#
# feet = StringVar()
# meters = StringVar()
# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
# feet_entry.grid(column=2, row=1, sticky=(W,E))
# ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
# ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
#
# ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
# ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
# for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
# feet_entry.focus()
# root.bind('<Return>', calculate)
#
#
# root.mainloop()


# root = Tk()
# root.title("radioButtons")
# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# secondframe = ttk.Frame(root, padding="3 3 12 12")
# secondframe.grid(column=1, row=0)
#
# phone = StringVar()
# home = ttk.Radiobutton(mainframe, text="Home", variable=phone, value='home').grid(column=3, row=1)
# office = ttk.Radiobutton(mainframe, text="Office", variable=phone, value='office').grid(column=1, row=1)
# cell = ttk.Radiobutton(mainframe, text='Mobile', variable=phone, value='cell').grid(column=1, row=2)
#
#
# ttk.Label(secondframe, text="secondary testing").grid(column=1, row=1)
# root.mainloop()



class degreeObject(object):

    def __init__(self, fullName, programOutcomes):
        self.fullName = fullName
        self.programOutcomes = programOutcomes


class outcomeButton(object):


    latestRow = 0

    def __init__(self, master, column, row):
        self.master = master
        self.var= IntVar()
        c = Checkbutton(
            master, text='Program Outcome {}'.format(row),
            variable=self.var,
            command=self.cb)
        c.grid(column=column, row=row)
        outcomeButton.latestRow = row if outcomeButton.latestRow < row else outcomeButton.latestRow


    def cb(self):
        print("Selected outcome {}".format(self.var))
        print(outcomeButton.latestRow)
        newButton = Checkbutton(
            self.master, text="newest outcome!",
        )
        newButton.grid(column=0, row=1+outcomeButton.latestRow)
        outcomeButton.latestRow += 1


def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))













webDev = degreeObject("Web Development", ["Web Dev outcome 1", "web dev outcome 2"])
cadd = degreeObject("CADD", ["cadd outcome 1", "cadd outcome 2"])
aced = degreeObject("ACED", ["aced outcome 1", "aced outcome 2"])


listOfDegrees = []
listOfDegrees.append(webDev)
listOfDegrees.append(cadd)
listOfDegrees.append(aced)


root = Tk()
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

degrees = Canvas(root, height=10)
dFrame = Frame(degrees)
dFrame.pack()

degrees.grid(column=0, row=0, sticky=(N, W, E, S))
degrees.configure(scrollregion=(0,0, 1000, 1000))
dScroll = ttk.Scrollbar(root, orient=VERTICAL, command=degrees.yview())
dScroll.grid(column=1, row=0, sticky=(N, S))
degrees.configure(yscrollcommand=dScroll.set)
degrees.create_window((4,4), window=dFrame, anchor='nw')

canvas = Canvas(root, height=5) # Holds program outcomes
frame = Frame(canvas)
frame.pack()
canvas.grid(column=2, row=0, sticky=(N, W, E, S))
canvas.configure(scrollregion=(0,0, 1000, 1000))




s = ttk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
s.grid(column=3, row=0, sticky=(N, S))
canvas.configure(yscrollcommand=s.set)
canvas.create_window((4,4), window=frame, anchor='nw')

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
for i in range(1, 20):

    newOutcome = outcomeButton(frame, 0, i)

root.mainloop()
