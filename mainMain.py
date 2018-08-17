import RetrieveProgramData as rpd
import ui






builder = rpd.RetrieveProgramData()
programGroupData = builder.buildProgramGroups()
programGroupData.sort(key=lambda x: x.programGroupTitle) # Alphabetizes the program group objects so the listbox won't


ui.UI(programGroupData)
