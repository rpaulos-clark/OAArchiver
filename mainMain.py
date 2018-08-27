import RetrieveProgramData as rpd
import ui


""" Should the user be allowed to pick a year/quarter assessed? Probably, otherwise we rely upon timely filing LOL

    - Storing .zip files in the database preserves the member names. Woo!
"""

builder = rpd.RetrieveProgramData()  # Pulls data from database. Loads into respective objects
programGroupData = builder.buildProgramGroups()
ui.UI(programGroupData)
