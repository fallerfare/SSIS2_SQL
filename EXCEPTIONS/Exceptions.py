from tkinter import messagebox
import re
from sqlalchemy import select
from DATA import GlobalDFs

connection = GlobalDFs.engine.connect()

# =======================
# ACCEPTED ENTRY FORMATS
# =======================
NormalEntry = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$")
ProgramEntry = re.compile(r"^Bachelor (of|Of) [A-Za-z\s\&\(\)]+$")
CollegeEntry = re.compile(r"^College (of|Of) [A-Za-z\s\&\(\)]+$")
IDEntry = re.compile(r"^\d{4}-\d{4}$")
EmailEntry = re.compile(r"^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}$")
CodeEntry = re.compile(r"^[A-Za-z]{3,6}$")
YearEntry = re.compile(r"^[1-5](st|nd|rd|th) (Year|Year and Above)$")
# =======================
# ACCEPTED ENTRY FORMATS
# =======================

# Bachelor Of Science In Business Administration (Business Economics)

# =======================
#      CHECK INPUTS
# =======================
def validate_inputs(input_dict):

    input_errors = []
    for label, (value, pattern) in input_dict.items():
        if not value.strip():  # Check if empty
            input_errors.append(f"{label} are empty!")
        elif not pattern.fullmatch(value):  # Check regex match
            input_errors.append(f"Invalid format for {label}!")
        
    if input_errors:
         raise ValueError("\n".join(input_errors))
    
# =======================
#      CHECK INPUTS
# =======================



# =======================
#      CHECK REMOVE
# =======================
    
def constraint_enrolled_program(programCode):
    checkStudents = select(GlobalDFs.studentsTable).where(GlobalDFs.studentsTable.c["Program Code"] == programCode)
    if connection.execute(checkStudents).fetchone():
        raise PermissionError(f"There are still Students currently enrolled in {programCode}!\nPlease Edit or Unenroll them First.")

def constraint_enrolled_college(collegeCode):
    checkStudents = select(GlobalDFs.studentsTable).where(GlobalDFs.studentsTable.c["College Code"] == collegeCode)
    if connection.execute(checkStudents).fetchone():
        raise PermissionError(f"There are still Students currently enrolled in {collegeCode}!\nPlease Edit or Unenroll them First.") 
    
# =======================
#      CHECK REMOVE
# =======================


# =======================
#      CHECK DUPES
# =======================

def validate_studentduplicates(studentID, edit = False, current_id = None):
    check = select(GlobalDFs.studentsTable).where(GlobalDFs.studentsTable.c["ID Number"] == studentID)
    duplicate = connection.execute(check).fetchone()
    if edit and duplicate and duplicate[0] == current_id:
        return
    if duplicate:
        raise ValueError(f"Student with ID Number {studentID} already exists!")   

def validate_programduplicates(programCode, edit = False, current_pcode = None):
    check = select(GlobalDFs.programsTable).where(GlobalDFs.programsTable.c["Program Code"] == programCode)
    duplicate = connection.execute(check).fetchone()
    if edit and duplicate and duplicate[0] == current_pcode:
        return
    if duplicate:
        raise ValueError(f"Program with Code {programCode} already exists!")
    
def validate_collegeduplicates(collegeCode, edit = False, current_ccode = None):
    check = select(GlobalDFs.collegesTable).where(GlobalDFs.collegesTable.c["College Code"] == collegeCode)
    duplicate = connection.execute(check).fetchone()
    if edit and duplicate and duplicate[0] == current_ccode:
        return
    if duplicate:
        raise ValueError(f"Program with Code {collegeCode} already exists!")

# =======================
#      CHECK DUPES
# =======================



# =======================
#     SHOW FUNCTIONS
# =======================
def show_removeerror_message(error):
    messagebox.showerror("Remove Error", str(error))

def show_inputerror_message(error):
    messagebox.showerror("Input Error", str(error))

def show_unexpected_error(error):
    messagebox.showerror("Unexpected Error", f"An error occurred: {str(error)}")
# =======================
#     SHOW FUNCTIONS
# =======================