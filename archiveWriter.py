# Ryan Paulos
# Clark College

import pyodbc
import re


class ArchiveWriter(object):
    def __init__(self, filePath, assessmentData, qtrAssessed, yearAssessed, supportFilePath):
        self.filePath = filePath
        self.fileName = self.parseFileName(filePath)
        self.assessmentData = assessmentData  # List of lists of Dicts: {ProgramID: List(outcomeIDs)
        self.qtrAssessed = qtrAssessed
        self.yearAssessed = yearAssessed
        self.supportFilePath = supportFilePath
        self.supportFileName = None  # Will be updated in loadSupportFile if applicable

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

        # Load report file data into memory
        with open(self.filePath, 'rb') as byteFile:  # load file data
            reportFileBytes = byteFile.read()

        # Load supporting documents. Returns None if no supporting document was passed
        supportFileBytes = self.loadSupportFile()

        # Load into the database
        # print(self.fileName)
        retVal = cursorProm.execute(
            r'INSERT INTO dbo.AssessmentReports'
            r'(ReportName, ReportBinary, QuarterAssessed, YearAssessed, SupportingDocuments, SupportingDocumentsName)'
            r' OUTPUT inserted.ReportID values (?, ?, ?, ?, ?, ?)',
            self.fileName, reportFileBytes, self.qtrAssessed, self.yearAssessed, supportFileBytes, self.supportFileName
        )
        primaryKey = retVal.fetchall()[0][0]  # ReportID

        # Now we upload the outcomes data
        for progGroupList in self.assessmentData:  # assessmentData contains lists organized by program group
            for progDict in progGroupList:  # Sort through each program in the program group
                for program, outcomes in progDict.items():  # Retrieve the key and the list of outcomeIDs
                    for outcome in outcomes:  # Iterate over the list of outcomeIDs
                        # print(primaryKey, program, outcome)
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

    def loadSupportFile(self):
        if not self.supportFilePath:
            return None
        with open(self.supportFilePath, 'rb') as supportFile:
            self.supportFileName = self.parseFileName(self.supportFilePath)
            return supportFile.read()

    @staticmethod
    def parseFileName(filePath):
        """
        Extracts the file name: The characters after the last '\'
        We are going to keep the file extension in case we allow other file extensions in the future

        :param filePath:  String
        :return: String
        """

        # First we try to isolate from normal a normal file path
        fileRE = re.compile(r'[^\\]*\..*')
        matchedRE = fileRE.search(filePath)
        fileName = matchedRE.group()

        if filePath == fileName:  # The file path used forward slashes, so we have to try again
            fileRE = re.compile(r'[^/]*\..*')
            matchedRE = fileRE.search(filePath)
            fileName = matchedRE.group()
        assert fileName is not None, "Failed to parse file name"
        return fileName
