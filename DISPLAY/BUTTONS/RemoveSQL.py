from tkinter import ttk, messagebox
from DATA import GlobalSQL
from EXCEPTIONS import ExceptionsSQL

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

        params = (self.removekey)

        match self.column_name:
            case "ID Number":
                query = f"DELETE FROM students WHERE `ID Number` = %s"

            case "Program Code":
                try:
                    ExceptionsSQL.constraint_enrolled_program(self.removekey)
                    query = f"DELETE FROM programs WHERE `Program Code` = %s"
                except PermissionError as pe:
                    ExceptionsSQL.show_removeerror_message(pe)
                    return

            case "College Code":
                try:
                    ExceptionsSQL.constraint_enrolled_college(self.removekey)
                    ExceptionsSQL.constraint_made_programs(self.removekey)
                    query = f"DELETE FROM colleges WHERE `College Code` = %s"
                except PermissionError as pe:
                    ExceptionsSQL.show_removeerror_message(pe)
                    return

            case _:
                return

        connection = GlobalSQL.return_connection()
      
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            connection.commit()
        finally:
            connection.close()

        self.table.PopulateTable(self.table.tree, GlobalSQL.updateDF(self.dataframe))
        self.removekey = None

# =====================
#    REMOVE BUTTON
# =====================      