from tkinter import *
from tkinter import ttk

""" 
    Solid as-is. Will now need to investigate creating outcomes canvas->frame->outcome checkboxes and toggling them
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
        self.programs = programs # list of program objects
        self.programBox = None # updated in _buildSelf
        self._buildSelf()

    def _buildSelf(self):
        """
            Alphabetizes program list and instantiates the programBox
        :return:
        """

        boxValues = [program.FullTitle for program in self.programs]
        boxValues.sort()
        boxValues = StringVar(value=boxValues)
        box = Listbox(self.root, listvariable=boxValues, height=self.height, width=self.width)
        box.grid(column=1, row=0)
        box.grid_remove()
        self.programBox = box

    def turnOn(self):
        self.programBox.grid()
        # Here we will turn on the outcomes canvas widget

    def turnOff(self):
        self.programBox.grid_remove()
        # Here we will turn off the outcomes canvas widget


class OutcomesCanvas(object):

    def __init__(self, master, programOutcomes):
        self.outcomes = programOutcomes # Looks like this will be a dict of outcomeID:Description




