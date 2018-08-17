import pyodbc, time

# conn_prom = pyodbc.connect(
#     r'DRIVER={ODBC Driver 11 for SQL Server};'
#     r'SERVER=prometheus;'
#     r'DATABASE=IRKanna;'
#     r'Trusted_connection=yes;')
# cursor_prom = conn_prom.cursor()
#
# # Run our stored procedure
# cursor_prom.execute("SELECT * FROM dbo.npsas2018DoneWithDupes")
# rows = cursor_prom.fetchall()



### Insertion begins here. Above code is for reference only
connProm = pyodbc.connect(
    r'DRIVER={ODBC DRiver 11 for SQL Server};'
    r'SERVER=prometheus;'
    r'DATABASE=IRKanna;'
    r'Trusted_connection=yes;'
)
cursorProm = connProm.cursor()

#
with open ("C:/testFolder/(BTEC).pdf", 'rb') as byteFile:
    data = byteFile.read()
    print(type(data))

#
pk = cursorProm.execute(
    r"INSERT INTO dbo.OutcomesAssessmentReportText OUTPUT inserted.ReportID values (?, ?)", 'BTEC', data
)

ret = pk.fetchall()
reportID = ret[0][0]
print(reportID)
test = connProm.commit()

#Works through here to write the file into the SQL database. Can we retrieve it and recreate the file now?

file = cursorProm.execute(
    r'SELECT ReportBinary '
    r'FROM IRKanna.dbo.OutcomesAssessmentReportText '
    r"WHERE ReportID = ?", '60'

)

bytesStream = file.fetchone()
print(type(bytesStream.ReportBinary))

with open("C:/testFolder/testFile.pdf", 'wb') as newFile:
    newFile.write(bytesStream.ReportBinary)

# I believe this all works. woot


