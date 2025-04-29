from tkinter import ttk
import tkinter as tk
from DATA import GlobalSQL
from EXCEPTIONS import ExceptionsSQL

class CreateCollgWindow:
    def __init__(self, table, Wintype):
        self.table          = table
        self.selectedtab    = self.table.tree.selection()
        self.item_values    = self.table.tree.item(self.selectedtab, "values")
        self.WinType        = Wintype

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
            self.Header                 = ttk.Label(self.frame, text="Add a College", font=('Arial', 20))
        elif self.WinType == "Edit":
            self.Header                 = ttk.Label(self.frame, text="Edit a College", font=('Arial', 20))

        # Labels
        self.CollegeNameLabel           = ttk.Label(self.frame, text="College Name", font=('Arial', 7))
        self.CollegeCodeLabel           = ttk.Label(self.frame, text="College Code", font=('Arial', 7))

        # Autofilled for Edit
        if self.WinType == "Edit":
            self.CollegeNameVar         = tk.StringVar(value=self.item_values[1])
            self.CollegeCodeVar         = tk.StringVar(value=self.item_values[0])
        else:
            self.CollegeNameVar         = tk.StringVar()
            self.CollegeCodeVar         = tk.StringVar()

        # EntryBoxes
        self.CollegeNameEntryBox        = ttk.Entry(self.frame, font=('Arial', 9), width=35, textvariable=self.CollegeNameVar)
        self.CollegeCodeEntryBox        = ttk.Entry(self.frame, font=('Arial', 9), width=35, textvariable=self.CollegeCodeVar)
        if self.WinType == "Edit":
            self.CollegeCodeEntryBox.config(state = "disabled")


        # Buttons
        if self.WinType == "Add":
            self.CreateCollgButton      = ttk.Button(self.frame, text="Add College",    command=self.CreateCollg)
        elif self.WinType == "Edit":
            self.CreateCollgButton      = ttk.Button(self.frame, text="Confirm Edit",   command=self.CreateCollg)

        self.cancelAction               = ttk.Button(self.frame, text="Cancel",         command=self.root.destroy)


        # GRID SETUP
        self.Header.grid(               row=0, column=0, columnspan=6, padx=20, pady=20)

        # Row 1
        self.CollegeNameEntryBox.grid(  row=1, column=0, columnspan=2, padx=7, pady=7, sticky='w')
        self.CollegeCodeEntryBox.grid(  row=1, column=2, columnspan=2, padx=7, pady=7, sticky='w')

        # Row 2
        self.CollegeNameLabel.grid(     row=2, column=0, columnspan=2, padx=5, pady=1, sticky='w')
        
        self.CollegeCodeLabel.grid(     row=2, column=2, columnspan=2, padx=5, pady=1, sticky='w')
        
        # Row 7
        self.cancelAction.grid(         row=7, column=2,                       pady=8, sticky='e')
        self.CreateCollgButton.grid(    row=7, column=3,                       pady=8, sticky='e')

        self.root.mainloop()

    def CreateCollg(self):
        try:
            college_name = self.CollegeNameEntryBox.get().strip()
            college_code = self.CollegeCodeEntryBox.get().strip()

            # Input validation
            ExceptionsSQL.validate_inputs({
                "College Name": (college_name, ExceptionsSQL.CollegeEntry),
                "College Code": (college_code, ExceptionsSQL.CodeEntry)
            })

            if self.WinType == "Add":
                # Check for duplicates
                ExceptionsSQL.validate_collegeduplicates(college_code)

                # Insert safely
                query = "INSERT INTO colleges (`College Code`, `College Name`) VALUES (%s, %s)"
                params = (college_code, college_name)

            elif self.WinType == "Edit":
                selected_item = self.table.tree.selection()
                item_values = self.table.tree.item(selected_item, "values")
                old_college_code = item_values[0]

                # Validate duplicates for edit
                ExceptionsSQL.validate_collegeduplicates(college_code, edit=True, current_ccode=old_college_code)

                query = "UPDATE colleges SET `College Name` = %s WHERE `College Code` = %s"
                params = (college_name, old_college_code)

            connection = GlobalSQL.return_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                connection.commit()
            finally:
                connection.close()

            # Refresh table
            self.table.PopulateTable(self.table.tree, GlobalSQL.readCollegesDF())
            self.root.destroy()

        except ValueError as ve:
            ExceptionsSQL.show_inputerror_message(ve)
        except Exception as e:
            ExceptionsSQL.show_unexpected_error(e)

        
