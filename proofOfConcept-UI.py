from tkinter import *
from tkinter import ttk



def toggleBoxes(*args):

   pass


class UI(object):

    def __init__(self, programGroupData):

        self.activeSecondary = None # We are electing to always have the first one active. Will be a box
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
            programs = programGroup.listPrograms()

            boxValues = StringVar(value=[program.FullTitle for program in programs])
            tempBox = Listbox(self.root, listvariable=boxValues, height=5, width=60)
            tempBox.grid(column=1, row=0)
            tempBox.grid_remove()
            self.programBoxes.append(tempBox)
            self.activeSecondary = self.programBoxes[0]
            self.programBoxes[0].grid()

        return

    def toggleBoxes(self, *args):

        i = self.masterBox.curselection()[0]

        if self.activeSecondary != self.programBoxes[i]:
            self.activeSecondary.grid_remove()
            self.programBoxes[i].grid()
            self.activeSecondary = self.programBoxes[i]
        else:
            pass

