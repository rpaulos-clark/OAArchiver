import RetrieveProgramData as rpd
import ui


""" BUG: Outcomes are sometimes switched between AAS and CP accounting. Build program groups uses a dictionary, so
    that is a likely candidate. Upgrade to 3.7 and that will probably resolve itself
"""

""" Should the user be allowed to pick a year/quarter assessed? Probably, otherwise we rely upon timely filing LOL
"""

builder = rpd.RetrieveProgramData()
programGroupData = builder.buildProgramGroups()
programGroupData.sort(key=lambda x: x.programGroupTitle) # Alphabetizes the program group objects so the listbox won't


ui.UI(programGroupData)
