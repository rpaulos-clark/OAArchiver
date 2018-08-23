import pyodbc
import time



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
        self.programGroups.sort(key=lambda x: x.programGroupTitle)
        return self.programGroups


class ProgramGroup(object):

    def __init__(self, programGroupEntries):
        self.programGroupTitle = programGroupEntries[0][2]
        self.programGroupID = programGroupEntries[0][0]
        self.programs = [] # Holds finished program objects
        self.programGroupEntries = programGroupEntries # Holds raw query rows
        self.buildPrograms()

    def buildPrograms(self):

        educationalIDs = {entry[1] for entry in self.programGroupEntries} # Set of programIDs

        # Group outcomes by program
        for id in educationalIDs:
            programEntries = [entry for entry in self.programGroupEntries if entry[1] == id]

            if programEntries:
                self.programs.append(Program(programEntries))
        self.programs.sort(key=lambda x: x.fullTitle)

    def assessedOutcomes(self):
        """

        :return: A list of dictionaries where each key is the programID and the entries are lists of outcomeIDs
        """
        assessedRaw = [program.assessedOutcomes() for program in self.programs]
        assessed = [program for program in assessedRaw if program is not None]
        if assessed:
            return assessed

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
        self.programEntries = programEntries # All query rows corresponding to this particular program
        self.educationalProgramID = programEntries[0][1] # EPC
        self.fullTitle = programEntries[0][3]
        self.programOutcomes = []
        self.buildOutcomes()

    def buildOutcomes(self):

        self.programOutcomes = [Outcome(entry[4], entry[5]) for entry in self.programEntries]
        self.programOutcomes.sort(key=lambda x: x.outcomeDescription)

    def assessedOutcomes(self):
        assessedRaw = [outcome.outcomeID for outcome in self.programOutcomes if outcome.assessed]  # All results
        assessed = [outcome for outcome in assessedRaw if outcome is not None]  # Filter the None values
        if assessed:
            return {self.educationalProgramID: assessed}

    # just messing around
    def __str__(self):
        return self.fullTitle


class Outcome(object):

    def __init__(self, outcomeID, outcomeDescription):
        self.outcomeID = outcomeID
        self.outcomeDescription = outcomeDescription
        self.assessed = False # To be toggled by the checkbox UI

