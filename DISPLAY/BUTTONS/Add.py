from tkinter import ttk
from DISPLAY.WINDOWS import SignUpSQL, CreateCollgSQL, CreateProgSQL
from DATA import GlobalSQL


# =====================
#     ADD BUTTON
# =====================
class Add:
    def __init__(self, root, dataframe, table):
        # Err you know innit
        self.root = root
        self.dataframe = GlobalSQL.updateDF(dataframe)
        self.table = table

        # Format Add Button according to tab
        match dataframe.columns[0]:  
            case "ID Number":
                command = lambda: SignUpSQL.SignUpWindow(self.table, "Add")
                buttext = "Enroll New"
            case "Program Code":
                command = lambda: CreateProgSQL.CreateProgWindow(self.table, "Add")
                buttext = "Add Program"
            case "College Code":
                command = lambda: CreateCollgSQL.CreateCollgWindow(self.table, "Add")
                buttext = "Add College"
            case _:
                buttext = "What, no button???"

        self.Button = ttk.Button(self.root, text=buttext, command=command)
# =====================
#     ADD BUTTON
# =====================