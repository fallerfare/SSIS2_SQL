from tkinter import ttk
import tkinter as tk
from DATA import GlobalDFs
from EXCEPTIONS import Exceptions
from sqlalchemy import create_engine, insert, update, Table, MetaData
from pymysql.err import IntegrityError

# ===================
#   STUDENT WINDOW
# ===================
class SignUpWindow:
    def __init__(self, table, Wintype):
        self.table          = table
        self.selectedtab    = self.table.tree.selection()
        self.item_values    = self.table.tree.item(self.selectedtab, "values")
        self.WinType        = Wintype

        # ================
        # MAIN WINDOW
        
        self.root           = tk.Toplevel()
        self.root.geometry( "900x400")
        self.root.resizable(width=False, height=False)
        self.frame          = ttk.Frame(self.root)
        self.frame.pack(    padx=20, pady=20, anchor="center")
        self.root.grab_set( ) 
        self.root.focus_set()  
        self.root.transient() 

        # MAIN WINDOW
        # ================



        # ================
        # WIDGETS

        # Header
        self.Header             = ttk.Label(self.frame, text="Welcome to MSU-IIT",      font=('Arial', 20))

        # Labels
        self.FirstNameLabel     = ttk.Label(self.frame, text="First Name",              font=('Arial', 7))
        self.LastNameLabel      = ttk.Label(self.frame, text="Last Name",               font=('Arial', 7))
        self.EmailLabel         = ttk.Label(self.frame, text="Email",                   font=('Arial', 7))
        self.IDLabel            = ttk.Label(self.frame, text="ID Number(YYYY-NNNN)",    font=('Arial', 7))
        self.GenderLabel        = ttk.Label(self.frame, text="Gender",                  font=('Arial', 7))
        self.CollegeLabel       = ttk.Label(self.frame, text="College",                 font=('Arial', 7))
        self.ProgramLabel       = ttk.Label(self.frame, text="Program",                 font=('Arial', 7))
        self.YearLabel          = ttk.Label(self.frame, text="Year Level",              font=('Arial', 7))

        # Autofilled for Edit
        if self.WinType == "Edit":
            self.IDVar          = tk.StringVar(value=self.item_values[0])
            self.FirstNameVar   = tk.StringVar(value=self.item_values[1])
            self.LastNameVar    = tk.StringVar(value=self.item_values[2])
            self.EmailVar       = tk.StringVar(value=self.item_values[3])
            self.YearVar        = tk.StringVar(value=self.item_values[4])
            self.GenderVar      = tk.StringVar(value=self.item_values[5]) 
            self.ProgramVar     = tk.StringVar(value=self.item_values[6])
            self.CollegeVar     = tk.StringVar(value=self.item_values[7])
            
        else:
            self.FirstNameVar   = tk.StringVar()
            self.LastNameVar    = tk.StringVar()
            self.EmailVar       = tk.StringVar()
            self.IDVar          = tk.StringVar()
            self.CollegeVar     = tk.StringVar()
            self.ProgramVar     = tk.StringVar()
            self.YearVar        = tk.StringVar()
            self.GenderVar      = tk.StringVar()

        # Entry Boxes
        self.FirstNameEntryBox  = ttk.Entry(self.frame, width=35,                       font=('Arial', 9), textvariable=self.FirstNameVar)
        self.LastNameEntryBox   = ttk.Entry(self.frame, width=35,                       font=('Arial', 9), textvariable=self.LastNameVar)
        self.EmailEntryBox      = ttk.Entry(self.frame, width=35,                       font=('Arial', 9), textvariable=self.EmailVar)
        self.IDEntryBox         = ttk.Entry(self.frame, width=35,                       font=('Arial', 9), textvariable=self.IDVar)

        # Dropdowns
        self.collegechoices     = list(GlobalDFs.readCollegesDF()['College Code'])
        self.programchoices     = []

        def collegechosen(event):
            College = self.CollegeEntryBox.get()

            # Filter programs based on selected college
            programsincollege = GlobalDFs.readProgramsDF()[GlobalDFs.readProgramsDF()['College Code'] == College]['Program Code'].tolist()
            self.ProgramEntryBox['values'] = programsincollege
            self.ProgramEntryBox.set('')
            # Filter programs based on selected college

        self.CollegeEntryBox    = ttk.Combobox( self.frame, state="readonly",
                                                values=self.collegechoices,
                                                width=35, textvariable=self.CollegeVar)

        self.CollegeEntryBox.bind("<<ComboboxSelected>>", collegechosen)

        self.ProgramEntryBox    = ttk.Combobox( self.frame, state="readonly",
                                                values=self.programchoices,
                                                width=35, textvariable=self.ProgramVar)

        self.YearEntryBox       = ttk.Combobox( self.frame, state="readonly",
                                                values=["1st Year", "2nd Year",
                                                        "3rd Year", "4th Year",
                                                        "5th Year and Above"],
                                                width=35, textvariable=self.YearVar)

        self.GenderEntryBox     = ttk.Combobox( self.frame, state="readonly",
                                                values=["Male", "Female", "Other"],
                                                width=35, textvariable=self.GenderVar)
        
        # Buttons
        if self.WinType == "Add":
            self.SignUpButton   = ttk.Button(self.frame, text="Enroll",         command=self.SignUp)
        
        elif self.WinType == "Edit":
            self.SignUpButton   = ttk.Button(self.frame, text="Confirm Edit",   command=self.SignUp)

        self.cancelAction       = ttk.Button(self.frame, text="Cancel",         command=self.root.destroy)

        # WIDGETS
        # ================


        # ================
        # GRID SETUP

        # Row 0
        self.Header.grid(           row=0, column=0, columnspan=6, padx=20, pady=20)

        # Row 1
        self.FirstNameEntryBox.grid(row=1, column=0, columnspan=2, padx=7, pady=7, sticky='w')
        self.LastNameEntryBox.grid( row=1, column=2, columnspan=2, padx=7, pady=7, sticky='w')
        self.CollegeEntryBox.grid(  row=1, column=4, columnspan=2, padx=7, pady=7, sticky='w')

        # Row 2
        self.FirstNameLabel.grid(   row=2, column=0, columnspan=2, padx=5, pady=1, sticky='w')
        self.LastNameLabel.grid(    row=2, column=2, columnspan=2, padx=5, pady=1, sticky='w')
        self.CollegeLabel.grid(     row=2, column=4, columnspan=2, padx=5, pady=1, sticky='w')

        # Row 3
        self.EmailEntryBox.grid(    row=3, column=0, columnspan=2, padx=7, pady=7, sticky='w')
        self.GenderEntryBox.grid(   row=3, column=2, columnspan=2, padx=2, pady=7, sticky='w')
        self.ProgramEntryBox.grid(  row=3, column=4, columnspan=2, padx=7, pady=7, sticky='w')

        # Row 4
        self.EmailLabel.grid(       row=4, column=0, columnspan=2, padx=5, pady=1, sticky='w')
        self.GenderLabel.grid(      row=4, column=2, columnspan=2, padx=5, pady=1, sticky='w')
        self.ProgramLabel.grid(     row=4, column=4, columnspan=2, padx=5, pady=1, sticky='w')

        # Row 5
        self.IDEntryBox.grid(       row=5, column=2, columnspan=2, padx=7, pady=7, sticky='w')
        self.YearEntryBox.grid(     row=5, column=4, columnspan=2, padx=7, pady=7, sticky='w')

        # Row 6
        self.IDLabel.grid(          row=6, column=2, columnspan=2, padx=5, pady=1, sticky='w')
        self.YearLabel.grid(        row=6, column=4, columnspan=2, padx=5, pady=1, sticky='w')

        # Row 7
        self.cancelAction.grid(     row=7, column=4,                       pady=8, sticky='e')
        self.SignUpButton.grid(     row=7, column=5,                       pady=8, sticky='e')

        self.root.mainloop()

        # GRID SETUP
        # ================

    # ================
    # SIGNUP   

    def SignUp(self):
        
        connection = GlobalDFs.engine.connect()

        try:

            # Get and clean entries
            ID_number       = self.IDEntryBox.get().strip()
            first_name      = self.FirstNameEntryBox.get().strip()
            last_name       = self.LastNameEntryBox.get().strip()
            email           = self.EmailEntryBox.get().strip()
            year_level      = self.YearEntryBox.get().strip()
            gender          = self.GenderEntryBox.get().strip()
            program_code    = self.ProgramEntryBox.get().strip()
            college_code    = self.CollegeEntryBox.get().strip()
            # Get and clean entries

            # Check entries' formats
            Exceptions.validate_inputs({
                    "ID Number"     : (ID_number,Exceptions.IDEntry),
                    "First Name"    : (first_name, Exceptions.NormalEntry),
                    "Last Name"     : (last_name, Exceptions.NormalEntry),
                    "Email"         : (email,Exceptions.EmailEntry),
                    "Year Level"    : (year_level, Exceptions.YearEntry),
                    "Gender"        : (gender, Exceptions.NormalEntry),
                    "Program Code"  : (program_code, Exceptions.CodeEntry),
                    "College Code"  : (college_code, Exceptions.CodeEntry)
            })
            # Check entries' formats

            # If window was called by ADD Button
            if(self.WinType == "Add"):
                Exceptions.validate_studentduplicates(ID_number)

                newStudent = insert(GlobalDFs.studentsTable).values(
                    **{
                        "ID Number"     : f"{ID_number}",
                        "First Name"    : f"{first_name}",
                        "Last Name"     : f"{last_name}",
                        "Email"         : f"{email}",
                        "Year Level"    : f"{year_level}",
                        "Gender"        : f"{gender}",
                        "Program Code"  : f"{program_code}",
                        "College Code"  : f"{college_code}"
                    }
                )

                connection.execute(newStudent)             
            # If window was called by ADD Button

            # If window was called by EDIT Button
            elif(self.WinType == "Edit"):
                selected_item = self.table.tree.selection()
                item_values = self.table.tree.item(selected_item, "values")
                old_ID_number = item_values[0]

                Exceptions.validate_studentduplicates(ID_number, edit = True, current_id = old_ID_number)

                editStudent = update(GlobalDFs.studentsTable).where(GlobalDFs.studentsTable.c["ID Number"] == old_ID_number).values(
                    **{
                        "ID Number"     : f"{ID_number}",
                        "First Name"    : f"{first_name}",
                        "Last Name"     : f"{last_name}",
                        "Email"         : f"{email}",
                        "Year Level"    : f"{year_level}",
                        "Gender"        : f"{gender}",
                        "Program Code"  : f"{program_code}",
                        "College Code"  : f"{college_code}"
                    }
                )
            
                connection.execute(editStudent)

            connection.commit()
            connection.close()
            self.table.PopulateTable(self.table.tree, GlobalDFs.readStudentsDF())
            self.root.destroy()

        except ValueError as ve:
            Exceptions.show_inputerror_message(ve)
        except Exception as e:
            Exceptions.show_unexpected_error(e)

    # SIGNUP
    # ================
# ===================
#   STUDENT WINDOW
# ===================