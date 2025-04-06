from tkinter import ttk, messagebox
from DATA import GlobalDFs
from DATA import GlobalHash
from EXCEPTIONS import Exceptions
from sqlalchemy import create_engine, delete, Table, MetaData

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
            case "ID Number":
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

        self.dataframe = GlobalDFs.updateDF(self.dataframe) 
        self.db_connection_str      = 'mysql+pymysql://root:root@localhost/studentdbms'
        self.db_connection          = create_engine(self.db_connection_str).connect()
        self.metadata               = MetaData()
        self.studentsTable          = Table('students', self.metadata, autoload_with=self.db_connection)
        self.programsTable          = Table('programs', self.metadata, autoload_with=self.db_connection)
        self.collegesTable          = Table('colleges', self.metadata, autoload_with=self.db_connection)

        # Match key to current tab
        match self.column_name:
            case "ID Number":
                # Remove the row
                self.removeAct      = delete(self.studentsTable).where(self.studentsTable.c["ID Number"] == self.removekey)
                
            case "Program Code":
                try:
                    Exceptions.validate_programremove(self.removekey)
                    # Remove the row
                    self.removeAct  = delete(self.programsTable).where(self.programsTable.c["Program Code"] == self.removekey)
                except PermissionError as pe:
                    Exceptions.show_removeerror_message(pe)

            case "College Code":
                try:
                    Exceptions.validate_collegeremove(self.removekey)
                    # Remove the row
                    self.removeAct  = delete(self.collegesTable).where(self.programsTable.c["College Code"] == self.removekey)
                except PermissionError as pe:
                    Exceptions.show_removeerror_message(pe)
                
        self.db_connection.execute(self.removeAct)
        self.db_connection.commit()
        self.table.PopulateTable(self.table.tree, GlobalDFs.updateDF(self.dataframe))
        self.removekey = None

# =====================
#    REMOVE BUTTON
# =====================      