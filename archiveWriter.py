import pyodbc
import re
import time

# @TODO: Wrap try/except clauses around the SQL database stuff in archiveFile in case of connection issues.
# @TODO: Clean this mess up now that we figured out what the problem was

class ArchiveWriter(object):

    def __init__(self, filePath, assessmentData):
        self.filePath = filePath
        self.fileName = self.parseFileName(filePath)
        self.assessmentData = assessmentData  # List of lists of Dicts: {ProgramID: List(outcomeIDs)
        self.archiveFile()

    def archiveFile(self):

        # Set up our SQL database connection
        connProm = pyodbc.connect(
            r'DRIVER={ODBC DRiver 11 for SQL Server};'
            r'SERVER=prometheus;'
            r'DATABASE=IRKanna;'  # -- This will hopefully be updated to reflect a dedicated location
            r'Trusted_connection=yes;'
        )
        cursorProm = connProm.cursor()

        # Load file data into memory
        with open(self.filePath, 'rb') as byteFile:  # load file data
            data = byteFile.read()

        # Load into the database
        #print(self.fileName)
        retVal = cursorProm.execute(
            r'INSERT INTO dbo.AssessmentReports(ReportName, ReportBinary) OUTPUT inserted.ReportID values (?, ?)',
            self.fileName, data
        )
        primaryKey = retVal.fetchall()[0][0]  # ReportID
        #print(primaryKey)

        # Now we upload the outcomes data
        for progGroupList in self.assessmentData:  # assessmentData contains lists organized by program group
            for progDict in progGroupList:  # Sort through each program in the program group
                for program, outcomes in progDict.items():  # Retrieve the key and the list of outcomeIDs
                    for outcome in outcomes:  # Iterate over the list of outcomeIDs
                        print(primaryKey, program, outcome)
                        cursorProm.execute(
                            r'INSERT INTO dbo.AssessmentReportsOutcomes(ReportID, EducationalProgramID, ProgramOutcomeID) '
                            r'values (?, ?, ?)', primaryKey, program, outcome
                        )
        connProm.commit()


        # Logs that we have successfully uploaded all relevant data.
        cursorProm.execute(
            r'INSERT INTO dbo.AssessmentReportUploadConfirmation(ReportID) values (?)', primaryKey
        )
        cursorProm.commit()
        return

    @staticmethod
    def parseFileName(filePath):
        """
        Extracts the file name: The characters after the last '\'
        We are going to keep the file extension in case we allow other file extensions in the future

        :param filePath:  String
        :return: String
        """

        # First we try to isolate from normal a normal file path
        fileRE = re.compile(r'[^\\]*.pdf')
        matchedRE = fileRE.search(filePath)
        fileName = matchedRE.group()

        if filePath == fileName:  # The file path used forward slashes, so we have to try again
            fileRE = re.compile(r'[^/]*.pdf')
            matchedRE = fileRE.search(filePath)
            fileName = matchedRE.group()
        assert fileName is not None, "Failed to parse file name"
        return fileName


