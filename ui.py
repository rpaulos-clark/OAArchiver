from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from archiveWriter import ArchiveWriter
""" 
    Resizing when an outcomesCanvas is removed/grid-ed is ANNOYING!
    
    Sizing issue where the checkboxes and text were off screen to the left appears to be because the canvas or frame 
    defaults to showing the view at the right-most point.
"""


class UI(object):

    def __init__(self, programGroupData):

        self.activeSecondary = None # We are electing to always have the first one active. Will be a box
        self.masterBox = None # instantated in buildMasterBox
        self.submitButton = None  #instantiated in buildSubmitButton
        self.fileButton = None  # instantiated in buildSelectFileButton
        self.filePath = None  # to be selected by the user
        self.programGroupData = programGroupData
        self.root = Tk()
        self.buildMasterBox()
        self.programBoxes = []
        self.buildProgramLBoxes()
        self.buildSubmitButton()
        self.buildSelectFileButton()


        #self.root.grid_columnconfigure(0, weight=1)
        #self.root.grid_rowconfigure(0, weight=1)
        self.root.state('zoomed') # makes fullscreen
        #self.root.attributes("-fullscreen", True)

        self.root.mainloop()

    def buildMasterBox(self):
        """
            Instantiate masterBox and populate with program group titles.
        :return:
        """
        listValues = StringVar(value=[progGroup.programGroupTitle for progGroup in self.programGroupData])
        masterBox = Listbox(self.root, listvariable=listValues, height=5, width=60)
        masterBox.grid(column=0, row=0, pady=400)  # pady prevents resize when switching prog groups
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

    def buildSubmitButton(self):

        button = Button(self.root, text='Submit Report', command=self.submit)
        button.grid(row=1, column=0)
        self.submitButton = button

    def buildSelectFileButton(self):
        button = Button(self.root, text='Select File to Save', command=self.selectFile)
        button.grid(row=1, column=1)
        self.fileButton = button

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

    def submit(self):
        """
            This method should gather the assessment data and verify that a filepath has been chosen before attempting
            the write to the database.
            :return:
        """
        if self.filePath is None:
            messagebox.showinfo(message="You must select a file to submit", icon='error')
            return

        assessmentData = self.assessedCensus()
        if not assessmentData:
            messagebox.showinfo(message="You must select at least one assessed program outcome")
            return

        # Pass data to archiveWriter(filePath, assessmentData)
        try:
            ArchiveWriter(self.filePath, assessmentData)
        except AssertionError:
            pass
            #Dialog box informing user of the problem.
        except Exception as e:
            pass
            # Dialog box - this should mean there was a problem commiting data to the database


        print("Submitting report!")

    def assessedCensus(self):
        """
            This method will be responsible for querying the programs for assessment information
            Call upon each ProgramBox to provide a list and join them together
        :return: A list of dictionaries: {EducationalProgramID: ProgramOutcomeID}
        """
        finalRaw = [progGroup.assessedOutcomes() for progGroup in self.programGroupData]
        final = [outcome for outcome in finalRaw if outcome is not None]
        return final

    # Receives filepath and ensures valid document type
    def selectFile(self):
        tempPath  = filedialog.askopenfilename()
        if tempPath == '':  # User pressed cancel
            return
        if tempPath[-4:] != '.pdf':
            messagebox.showinfo(message="Invalid file format; file must be PDF format", icon='error')
        else:
            self.filePath = tempPath
        return


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

        boxValues = [program.fullTitle for program in self.programs]
        #boxValues.sort()  # Believe this to be the cause of Program/Program Canvas mismatches
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
            self.activeCanvas = None


class OutcomesCanvas(object):

    def __init__(self, master, programOutcomes):
        self.root = master
        self.outcomes = programOutcomes  # Looks like this will be a dict of outcomeID:Description
        self.canvas = None  # Updated in buildself
        self.frame = None  # updated in buildSelf
        self.vBar = None  # updated in buildSelf
        self.hBar = None  # updated in buildself
        self.buildSelf()
        self.populateFrame()

    def buildSelf(self):
        # Construct master canvas
        canvas = Canvas(self.root, width=600, height=600)
        canvas.grid(column=2, row=0, padx=20)
        canvas.grid_remove()

        # Add vertical scrollbar
        vBar = ttk.Scrollbar(self.root, orient=VERTICAL, command=canvas.yview)
        vBar.grid(column=3, row=0, sticky=(N, S))  # maybe take out sticky
        canvas.configure(yscrollcommand=vBar.set)
        vBar.grid_remove()

        # Add horizontal scrollbar
        hBar = ttk.Scrollbar(self.root, orient=HORIZONTAL, command=canvas.xview)
        hBar.grid(column=2, row=1, sticky=(W, E))
        canvas.configure(xscrollcommand=hBar.set)
        hBar.grid_remove()


        # Add frame
        frame = ttk.Frame(canvas)
        canvas.create_window((20, 20), window=frame)  # Hang the frame
        frame.bind("<Configure>", lambda event, canvas=canvas: self.onFrameConfigure(canvas))  # accommodate new widgets
        #canvas.bind("<Configure>", lambda event, canvas=canvas: self.onFrameConfigure(canvas)) ## Test. This is likely unnecessary, was trying to figure out why the text was off.

        self.canvas = canvas
        self.frame = frame
        self.vBar = vBar
        self.hBar = hBar

    def populateFrame(self):
        #  Here we will populate the canvas' frame with OutcomeButtons

        i = 0
        for outcome in self.outcomes:
            OutcomeButton(self.frame, outcome, i)
            i += 1

    def turnOn(self):
        self.canvas.grid()
        self.vBar.grid()
        self.hBar.grid()
        self.canvas.xview("moveto", 0.0)  # SALVATION!! Focuses the canvas all the way to the left side

    def turnOff(self):
        self.canvas.grid_remove()
        self.vBar.grid_remove()
        self.hBar.grid_remove()

    def onFrameConfigure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))


# Accepts an outcome object to populate the UI portion and for communicating the toggle states
class OutcomeButton(object):

    def __init__(self, master, outcome, row):
        self.master = master
        self.outcome = outcome
        self.row = row
        self.button = None  # Instantiated in buildSelf
        self.var = IntVar()  # Attempting to debug overlapping/duplicate checked boxes. Fixed, probably not cuz of this, but I'm leaving it. ALthough maybe it doens't internally track state and did need this...
        self.buildSelf()

    def buildSelf(self):
        button = Checkbutton(
            self.master, text=self.outcome.outcomeDescription, command=self.toggleAssessed, variable=self.var)
        button.grid(column=3, row=self.row, sticky=W)
        self.button = button

    def toggleAssessed(self):
        if self.outcome.assessed:
            self.outcome.assessed = False
        else:
            self.outcome.assessed = True
