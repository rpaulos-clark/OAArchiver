from tkinter import *
from tkinter import ttk

""" 
    Resizing when an outcomesCanvas is removed/grid-ed is ANNOYING!
"""


class UI(object):

    def __init__(self, programGroupData):

        self.activeSecondary = None # We are electing to always have the first one active. Will be a box
        self.masterBox = None # instantated in buildMasterBox
        self.programGroupData = programGroupData
        self.root = Tk()
        self.buildMasterBox()
        self.programBoxes = []
        self.buildProgramLBoxes()

        self.root.mainloop()

    def buildMasterBox(self):
        """
            Instantiate masterBox and populate with program group titles.
        :return:
        """
        listValues = StringVar(value=[progGroup.programGroupTitle for progGroup in self.programGroupData])
        masterBox = Listbox(self.root, listvariable=listValues, height=5, width=60)
        masterBox.grid(column=0, row=0)
        masterBox.bind("<Double-1>", self.toggleBoxes)
        self.masterBox = masterBox

        return

    def buildProgramLBoxes(self):

        for programGroup in self.programGroupData:
            programs = programGroup.listPrograms() # Retrieves all program objects
            tempBox = ProgramBox(programs, self.root, 5, width=60)
            self.programBoxes.append(tempBox)
            self.activeSecondary = self.programBoxes[0]
            self.activeSecondary.turnOn()

        return

    def toggleBoxes(self, *args):
        """
            Control logic for displaying the program box
        :param args:  I just copied that from an example. Probably unnecessary
        :return:
        """
        i = self.masterBox.curselection()[0]

        if self.activeSecondary is not self.programBoxes[i]:
            self.activeSecondary.turnOff()
            self.activeSecondary = self.programBoxes[i]
            self.activeSecondary.turnOn()
        else:
            pass

    def assessedCensus(self):
        """
            This method will be responsible for querying the programs for assessment information
            Call upon each ProgramBox to provide a list and join them together
        :return:
        """


class ProgramBox(object):

    def __init__(self, programs, master, height, width):
        """
            Box defaults to removed status

        :param programs: List of program objects
        :param master: widget master
        :param height:
        :param width:
        """
        self.root = master
        self.height = height
        self.width = width
        self.programs = programs  # list of program objects
        self.programBox = None  # updated in _buildSelf
        self.outcomeCanvases = []  # updated in buildCanvases
        self.activeCanvas = None  # Currently displayed canvas
        self._buildSelf()
        self.buildCanvases()

        # here we will build an outcomes canvas

    def _buildSelf(self):
        """
            Alphabetizes program list and instantiates the programBox
        :return:
        """

        boxValues = [program.FullTitle for program in self.programs]
        boxValues.sort()
        boxValues = StringVar(value=boxValues)
        box = Listbox(self.root, listvariable=boxValues, height=self.height, width=self.width)
        box.bind("<Double-1>", self.toggleCanvases)
        box.grid(column=1, row=0)
        box.grid_remove()
        self.programBox = box

    def buildCanvases(self):
        self.outcomeCanvases = [OutcomesCanvas(self.root, program.programOutcomes) for program in self.programs]

    def toggleCanvases(self, *args):

        i = self.programBox.curselection()[0]

        if self.activeCanvas is None:  # Account for blank canvas
            self.activeCanvas = self.outcomeCanvases[i]
            self.activeCanvas.turnOn()
            return

        if self.activeCanvas is not self.outcomeCanvases[i]:  # Swap out active canvases
            self.activeCanvas.turnOff()
            self.activeCanvas = self.outcomeCanvases[i]
            self.activeCanvas.turnOn()

    def turnOn(self):
        self.programBox.grid()

    def turnOff(self):
        self.programBox.grid_remove()
        if self.activeCanvas is not None:
            self.activeCanvas.turnOff()


class OutcomesCanvas(object):

    def __init__(self, master, programOutcomes):
        self.root = master
        self.outcomes = programOutcomes  # Looks like this will be a dict of outcomeID:Description
        self.canvas = None  # Updated in buildself
        self.frame = None  # updated in buildSelf
        self.vBar = None  # updated in buildSelf
        self.buildSelf()
        self.populateFrame()

    def buildSelf(self):
        # Construct master canvas
        canvas = Canvas(self.root, width=600)
        canvas.grid(column=2, row=0)
        canvas.grid_remove()
        canvas.configure(scrollregion=(0, 0, 1000, 1000))  # Not sure what I want to do with this. Come back -- 8/17/2018

        # Add scrollbar
        vBar = ttk.Scrollbar(self.root, orient=VERTICAL, command=canvas.yview)
        vBar.grid(column=3, row=0, sticky=(N, S))  # maybe take out sticky
        canvas.configure(yscrollcommand=vBar.set)
        vBar.grid_remove()

        # Add frame
        frame = ttk.Frame(canvas)
        canvas.create_window((4, 4), window=frame)  # Hang the frame
        frame.bind("<Configure>", lambda event, canvas=canvas: self.onFrameConfigure(canvas))  # accommodate new widgets

        self.canvas = canvas
        self.frame = frame
        self.vBar = vBar

    def populateFrame(self):
        #  Here we will populate the canvas' frame with OutcomeButtons

        i = 0
        for outcome in self.outcomes:
            OutcomeButton(self.frame, outcome, i)
            i += 1

    def turnOn(self):
        self.canvas.grid()
        self.vBar.grid()

    def turnOff(self):
        self.canvas.grid_remove()
        self.vBar.grid_remove()

    def onFrameConfigure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))


# Accepts an outcome object to populate the UI portion and for communicating the toggle states
class OutcomeButton(object):

    def __init__(self, master, outcome, row):
        self.master = master
        self.outcome = outcome
        self.row = row
        self.button = None  # Instantiated in buildSelf
        self.buildSelf()

    def buildSelf(self):
        button = Checkbutton(self.master, text=self.outcome.outcomeDescription, command=self.toggleAssessed)
        button.grid(column=3, row=self.row)

    def toggleAssessed(self):
        if self.outcome.assessed:
            self.outcome.assessed = False
        else:
            self.outcome.assessed = True
