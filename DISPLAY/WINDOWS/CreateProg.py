from tkinter import ttk
import tkinter as tk
from DATA import GlobalDFs
from EXCEPTIONS import Exceptions
from sqlalchemy import insert, update

# ===================
#   PROGRAM WINDOW
# ===================
class CreateProgWindow:
    def __init__(self, table, Wintype):
        self.table          = table
        self.selectedtab    = self.table.tree.selection()
        self.item_values    = self.table.tree.item(self.selectedtab, "values")
        self.WinType        = Wintype

        # MAIN WINDOW
        self.root           = tk.Toplevel()
        self.root.geometry( "900x400")
        self.root.resizable(width=False, height=False)

        self.frame          = ttk.Frame(self.root)
        self.frame.pack(    padx=20, pady=20, anchor="center")

        self.root.grab_set( ) 
        self.root.focus_set()  
        self.root.transient() 

        # WIDGETS

        # Header
        if self.WinType == "Add":
            self.Header                 = ttk.Label(self.frame, text="Add a Program",   font=('Arial', 20))
        elif self.WinType == "Edit":
            self.Header                 = ttk.Label(self.frame, text="Edit a Program",  font=('Arial', 20))
        

        # Labels
        self.ProgramNameLabel           = ttk.Label(self.frame, text="Program Name",    font=('Arial', 7))
        self.ProgramCodeLabel           = ttk.Label(self.frame, text="Program Code",    font=('Arial', 7))
        self.CollegeLabel               = ttk.Label(self.frame, text="College",         font=('Arial', 7))

        # Autofilled for Edit
        if self.WinType == "Edit":
            self.ProgramNameVar         = tk.StringVar(value=self.item_values[1])
            self.ProgramCodeVar         = tk.StringVar(value=self.item_values[0])
            self.CollegeCodeVar         = tk.StringVar(value=self.item_values[2])
        else:
            self.ProgramNameVar         = tk.StringVar()
            self.ProgramCodeVar         = tk.StringVar()
            self.CollegeCodeVar         = tk.StringVar()

        # EntryBoxes
        self.ProgramNameEntryBox        = ttk.Entry(self.frame, font=('Arial', 9), width=35, textvariable=self.ProgramNameVar)
        self.ProgramCodeEntryBox        = ttk.Entry(self.frame, font=('Arial', 9), width=35, textvariable=self.ProgramCodeVar)
        if self.WinType == "Edit":
            self.ProgramCodeEntryBox.config(state = "disabled")

        # Dropdowns
        self.collegechoices             = list(GlobalDFs.readCollegesDF()['College Code'])
        self.CollegeEntryBox            = ttk.Combobox(self.frame, state="readonly", values=self.collegechoices, width=35, textvariable=self.CollegeCodeVar)

        # Buttons
        if self.WinType     == "Add":
            self.CreateProgButton       = ttk.Button(self.frame, text="Add Program",    command=self.CreateProg)
        elif self.WinType   == "Edit":
            self.CreateProgButton       = ttk.Button(self.frame, text="Confirm Edit",   command=self.CreateProg)

        self.cancelAction               = ttk.Button(self.frame, text="Cancel",         command=self.root.destroy)


        # GRID SETUP
        # Row 0
        self.Header.grid(               row=0, column=0, columnspan=6, padx=20, pady=20)

        # Row 1
        self.ProgramNameEntryBox.grid(  row=1, column=0, columnspan=2, padx=7, pady=7, sticky='w')
        self.ProgramCodeEntryBox.grid(  row=1, column=2, columnspan=2, padx=7, pady=7, sticky='w')
        self.CollegeEntryBox.grid(      row=1, column=4, columnspan=2, padx=7, pady=7, sticky='w')

        # Row 2
        self.ProgramNameLabel.grid(     row=2, column=0, columnspan=2, padx=5, pady=1, sticky='w')
        self.ProgramCodeLabel.grid(     row=2, column=2, columnspan=2, padx=5, pady=1, sticky='w')
        self.CollegeLabel.grid(         row=2, column=4, columnspan=2, padx=5, pady=1, sticky='w')

        # Row 7
        self.cancelAction.grid(         row=7, column=4,                       pady=8, sticky='e')
        self.CreateProgButton.grid(     row=7, column=5,                       pady=8, sticky='e')

        self.root.mainloop()

    def CreateProg(self):

        connection = GlobalDFs.engine.connect()
       
        try:
            program_name = self.ProgramNameEntryBox.get().strip()
            program_code = self.ProgramCodeEntryBox.get().strip()
            college_code = self.CollegeEntryBox.get().strip()
            
            Exceptions.validate_inputs({
                                        "Program Name" : (program_name, Exceptions.ProgramEntry),
                                        "Program Code" : (program_code, Exceptions.CodeEntry),
                                        "College Code" : (college_code, Exceptions.CodeEntry)
            })  

            if self.WinType == "Add":
                Exceptions.validate_programduplicates(program_code)
                
                newProgram = insert(GlobalDFs.programsTable).values(
                    **{
                        "Program Name"  : f"{program_name}",
                        "Program Code"  : f"{program_code}",
                        "College Code"  : f"{college_code}"
                    }
                )

                connection.execute(newProgram) 
                
            elif self.WinType == "Edit":
                selected_item = self.table.tree.selection()
                item_values = self.table.tree.item(selected_item, "values")
                old_program_code = item_values[0]
                Exceptions.validate_programduplicates(program_code, edit = True, current_pcode = old_program_code)

                editProgram = update(GlobalDFs.programsTable).where(GlobalDFs.programsTable.c["Program Code"] == old_program_code).values(
                    **{
                        "Program Code"  : f"{program_code}",
                        "Program Name"  : f"{program_name}",
                        "College Code"  : f"{college_code}"
                    }
                )
            
                connection.execute(editProgram)              
                 
            connection.commit()
            connection.close()
            self.table.PopulateTable(self.table.tree, GlobalDFs.readProgramsDF())
            self.root.destroy()
            
        
        except ValueError as ve:
            Exceptions.show_inputerror_message(ve)
        except Exception as e:
            Exceptions.show_unexpected_error(e)
# ===================
#   PROGRAM WINDOW
# ===================