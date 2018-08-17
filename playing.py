from tkinter import *
from tkinter import ttk



"""" 
    Solid progress made here. Don't mess with it anymore.
    Despite the file name, this is important for the future work
"""

class degreeObject(object):

    def __init__(self, fullName, programOutcomes):
        self.fullName = fullName
        self.programOutcomes = programOutcomes


class outcomeButton(object):


    latestRow = 0

    def __init__(self, master, column, text):
        self.master = master
        self.var= IntVar()
        c = Checkbutton(
            master, text=text,
            variable=self.var,
            command=self.cb)
        c.grid(column=column, row=outcomeButton.latestRow, sticky=W)
        outcomeButton.latestRow += 1

    def cb(self):
        print("outcome toggled")
        print(self.var.get())
        # print("Selected outcome {}".format(self.var))
        # print(outcomeButton.latestRow)
        # newButton = Checkbutton(
        #     self.master, text="newest outcome!",
        # )
        # newButton.grid(column=0, row=1+outcomeButton.latestRow)
        # outcomeButton.latestRow += 1


def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))



def displayDegreeOutcomes(*args):
    i = lbox.curselection()[0]

    selectedDegree = listOfDegrees[i]
    for outcome in selectedDegree.programOutcomes:
        print(outcome)


def populateOutcomes(*args):
    i = lbox.curselection()[0]

    selectedDegree = listOfDegrees[i]
    for outcome in selectedDegree.programOutcomes:
        outcomeButton(outcomeFrame, 0, outcome)


root = Tk()


webDev = degreeObject("Web Development", ["web wev outcome 1", "web dev outcome 2"])
cadd = degreeObject("CADD", ["cadd outcome 1", "cadd outcome 2"])
aced = degreeObject("ACED", ["aced outcome 1", "aced outcome 2"])
weld = degreeObject("welding", ["weld outcome 1", "weld outcome 2"])
surveying = degreeObject("surveying", ["surveying outcome 1", "surveying outcome 2"])
auto = degreeObject("Automotive", ["auto outcome 1", "automotive outcome 2"])


listOfDegrees = []
listOfDegrees.append(webDev)
listOfDegrees.append(cadd)
listOfDegrees.append(aced)
listOfDegrees.append(weld)
listOfDegrees.append(surveying)
listOfDegrees.append(auto)


# We must construct a list/tuple of degree names to be used in the listBox
dNames = []
for degree in listOfDegrees:
    dNames.append(degree.fullName)

listBoxValues = StringVar(value=dNames)

# Now we begin constructing the UI
# Grid and content Frame
degreeFrame = ttk.Frame(root, padding="3 3 12 12")
degreeFrame.grid(column=0, row=1, sticky=(N, E, S, W))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)


# Create our listbox and its label
lbox = Listbox(degreeFrame, listvariable=listBoxValues, height=5)
lboxLabel = ttk.Label(root, text="Select Degree", anchor=NW)


# grid the label and lbox
lboxLabel.grid(column=0, row=0, sticky=N)
lbox.grid(column=0, row=1, sticky=(N, W))

# Bind the listbox
lbox.bind('<Double-1>', populateOutcomes)





# Now we will create the outcome portion of the UI
outcomeCanvas = Canvas(root)
outcomeCanvas.grid(column=1, row=1)
outcomeLabel = ttk.Label(root, text="Outcomes")
outcomeFrame = ttk.Frame(outcomeCanvas)
#outcomeCanvas.create_window((0,0), window=outcomeFrame, anchor=NW)

vBar = ttk.Scrollbar(root, orient=VERTICAL, command=outcomeCanvas.yview)
vBar.grid(column=2, row=1, sticky=(N, S))
outcomeCanvas.configure(yscrollcommand=vBar.set)

outcomeCanvas.create_window((4,4,), window=outcomeFrame)
outcomeFrame.bind("<Configure>", lambda event, canvas=outcomeCanvas: onFrameConfigure(canvas))

outcomeLabel.grid(column=1, row=0, sticky=(N, W))
outcomeCanvas.configure(scrollregion=(0,0,1000,1000))


# Now lets populate the outcomes

root.mainloop()
# root = Tk()
# root.grid_columnconfigure(0, weight=1)
# root.grid_rowconfigure(0, weight=1)
#
# degrees = Canvas(root, height=10)
# dFrame = Frame(degrees)
# dFrame.pack()
#
# degrees.grid(column=0, row=0, sticky=(N, W, E, S))
# degrees.configure(scrollregion=(0,0, 1000, 1000))
# dScroll = ttk.Scrollbar(root, orient=VERTICAL, command=degrees.yview())
# dScroll.grid(column=1, row=0, sticky=(N, S))
# degrees.configure(yscrollcommand=dScroll.set)
# degrees.create_window((4,4), window=dFrame, anchor='nw')
#
# canvas = Canvas(root, height=5) # Holds program outcomes
# frame = Frame(canvas)
# frame.pack()
# canvas.grid(column=2, row=0, sticky=(N, W, E, S))
# canvas.configure(scrollregion=(0,0, 1000, 1000))
#
#
#
#
# s = ttk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
# s.grid(column=3, row=0, sticky=(N, S))
# canvas.configure(yscrollcommand=s.set)
# canvas.create_window((4,4), window=frame, anchor='nw')
#
# frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
# for i in range(1, 20):
#
#     newOutcome = outcomeButton(frame, 0, i)
#
# root.mainloop()
