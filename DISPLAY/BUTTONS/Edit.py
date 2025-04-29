from tkinter import ttk
from DISPLAY.WINDOWS import SignUp, CreateCollg, CreateProg
from DATA import GlobalSQL

# =====================
#    EDIT BUTTON
# =====================
class Edit:
    def __init__(self, root, dataframe, table):
        # ye
        self.root = root
        self.dataframe = GlobalSQL.updateDF(dataframe)
        self.table = table

        # Format Add Button according to tab
        match dataframe.columns[0]:  
            case "ID Number":
                command = lambda: SignUp.SignUpWindow(self.table, "Edit")
                buttext = "Edit Student"
            case "Program Code":
                command = lambda: CreateProg.CreateProgWindow(self.table, "Edit")
                buttext = "Edit Program"
            case "College Code":
                command = lambda: CreateCollg.CreateCollgWindow(self.table, "Edit")
                buttext = "Edit College"
            case _:
                buttext = "What, no button???"

        self.Button = ttk.Button(self.root, text=buttext, command=command)
# =====================
#    EDIT BUTTON
# =====================