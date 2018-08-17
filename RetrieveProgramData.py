import pyodbc
import time


"""
    Seems to work as intended at present. Should we create an Outcome object? not sure   
"""


class RetrieveProgramData(object):

    def __init__(self):

        self.pyodbcTuples = []
        self.programGroups = []
        self.pullData() # Updates pyodbcRows with data

    def pullData(self):

        """
            Updates self with the tupled pyodbc rows from the below sql query
        """

        try:
            connProm = pyodbc.connect(
                r'DRIVER={ODBC DRiver 11 for SQL Server};'
                r'SERVER=prometheus;'
                r'DATABASE=IRKanna;'
                r'Trusted_connection=yes;'
            )
            cursorProm = connProm.cursor()
            cursorProm.execute("""
                select 
                    pg.ProgramGroupID
                    ,pg.EducationalProgramID
                    ,pg.ProgramGroupTitle
                    ,pg.FullTitle
                    ,po.ProgramOutcomeID
                    ,po.Description
                    
                from Program.dbo.vw_ProgramAndGroup pg
                inner join Program.dbo.vw_public_ProgramOutcome_getActive po
                on pg.EducationalProgramID = po.EducationalProgramID
                order by pg.ProgramGroupID, pg.EducationalProgramID
            
            """
            )
        except:
            print("Error connecting to SQL Server...terminating")
            time.sleep(10)
            exit(1)

        pyodbcRows = cursorProm.fetchall() # program will have exited if that isn't instantiated
        for row in pyodbcRows:
            self.pyodbcTuples.append(tuple(row))
        return

    def buildProgramGroups(self):

        """

            Here we must determine how to separate the different program groups and create their respective objects
        """

        programIDs = {row[0] for row in self.pyodbcTuples} #  ProgramGroupID set

        # separate and group all entries by ProgramGroupID, then use the groups to create the programs
        for id in programIDs:
            programGroupEntries = [entry for entry in self.pyodbcTuples if entry[0] == id]
            self.programGroups.append(ProgramGroup(programGroupEntries))

        return self.programGroups


class ProgramGroup(object):

    def __init__(self, programGroupEntries):
        self.programGroupTitle = programGroupEntries[0][2]
        self.programGroupID = programGroupEntries[0][0]
        self.programs = [] # Holds finished program objects
        self.programGroupEntries = programGroupEntries # Holds raw query rows
        self.buildPrograms()

    def buildPrograms(self):

        educationalIDs = {entry[1] for entry in self.programGroupEntries}

        # Group outcomes by program
        for id in educationalIDs:
            programEntries = [entry for entry in self.programGroupEntries if entry[1] == id]

            if programEntries:
                self.programs.append(Program(programEntries))

    def listPrograms(self):

        return [program for program in self.programs]

    # Just messing around
    def printPrograms(self):
        for program in self.programs:
            print(program)
            program.printOutcomes()


class Program(object):

    def __init__(self, programEntries):
        """

        :param programEntries: A list of all query entries corresponding to ONE program (i.e. all program outcomes)
        """
        self.programEntries = programEntries
        self.educationalProgramID = programEntries[0][1] # EPC
        self.FullTitle = programEntries[0][3]
        self.programOutcomes = {} # becomes a dict of outcomeID:Descriptions.
        self.buildOutcomes()

    def buildOutcomes(self):

        # outcomeID:outcome text
        self.programOutcomes = {entry[4]: entry[5] for entry in self.programEntries}

    # Just messing around
    def printOutcomes(self):

        for keys, values in self.programOutcomes.items():
            print(keys, values)

    # just messing around
    def __str__(self):
        return self.FullTitle



