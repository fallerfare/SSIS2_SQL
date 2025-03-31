from tkinter import ttk, messagebox
from DATA import GlobalDFs
from DATA import GlobalHash
from EXCEPTIONS import Exceptions

# =====================
#    REMOVE BUTTON
# =====================

class Remove:
    def __init__(self, root, dataframe, table):
        # tommy innit
        self.root = root
        self.dataframe = dataframe
        self.table = table
        self.removekey = None 
        self.column_name = self.dataframe.columns[0]

        # Format Remove Button according to tab
        match self.column_name:  
            case "ID":
                buttext = "Remove Student"
            case "Program Code":
                buttext = "Remove Program"
            case "College Code":
                buttext = "Remove College"
            case _:
                buttext = "What, no button???"

        self.Button = ttk.Button(self.root, text=buttext, command=self.confirmRemove, state="disabled")

    # we removin dis guy
    # accessed by treeviewselect
    def setremovekey(self, key):
        self.removekey = key

        # Debugging
        # print("Setting: " + self.removekey)

    def confirmRemove(self):
        confirm = messagebox.askyesno("Confirm", "Confirm Remove?")
        if confirm is True:
            self.remove_entry()
        elif confirm is False:
            return

    # dis guy be removed
    def remove_entry(self):
        if self.removekey is None:
            return
        
        # Debugging
        # print("Removing: " + self.removekey)

        self.dataframe = GlobalDFs.updateDF(self.dataframe) # Is this needed? idk but it make me feel safe. Applies to other uses TTOTT

        # Match key to current tab
        match self.column_name:
            case "ID":
                # Remove the row
                self.dataframe = self.dataframe[self.dataframe[self.column_name] != self.removekey]
                GlobalDFs.writeStudentsDF(self.dataframe)
                self.table.Populate(self.table.tree, GlobalDFs.readStudentsDF(), "Update")
            case "Program Code":
                try:
                    Exceptions.validate_programremove(self.removekey)
                    # Remove the row
                    self.dataframe = self.dataframe[self.dataframe[self.column_name] != self.removekey]
                    GlobalDFs.writeProgramsDF(self.dataframe)     
                    self.table.Populate(self.table.tree, GlobalDFs.readProgramsDF(), "Update")
                except PermissionError as pe:
                    Exceptions.show_removeerror_message(pe)
            case "College Code":
                try:
                    Exceptions.validate_collegeremove(self.removekey)
                    # Remove the row
                    self.dataframe = self.dataframe[self.dataframe[self.column_name] != self.removekey]
                    GlobalDFs.writeCollegesDF(self.dataframe)
                    self.table.Populate(self.table.tree, GlobalDFs.readCollegesDF(), "Update")
                except PermissionError as pe:
                    Exceptions.show_removeerror_message(pe)
                

        self.removekey = None

# =====================
#    REMOVE BUTTON
# =====================      