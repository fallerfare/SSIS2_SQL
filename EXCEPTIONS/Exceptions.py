from tkinter import messagebox
import re
from sqlalchemy import create_engine, Table, MetaData, select

db_connection_str      = 'mysql+pymysql://root:root@localhost/studentdbms'
db_connection          = create_engine(db_connection_str).connect()
metadata               = MetaData()
collegesTable          = Table('colleges', metadata, autoload_with=db_connection)
programsTable          = Table('programs', metadata, autoload_with=db_connection)
studentsTable          = Table('students', metadata, autoload_with=db_connection)

# =======================
# ACCEPTED ENTRY FORMATS
# =======================
NormalEntry = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$")
ProgramEntry = re.compile(r"^Bachelor (of|Of) [A-Za-z\s]+$")
CollegeEntry = re.compile(r"^College (of|Of) [A-Za-z\s]+$")
IDEntry = re.compile(r"^\d{4}-\d{4}$")
EmailEntry = re.compile(r"^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}$")
CodeEntry = re.compile(r"^[A-Za-z]{3,6}$")
YearEntry = re.compile(r"^[1-5](st|nd|rd|th) (Year|Year and Above)$")
# =======================
# ACCEPTED ENTRY FORMATS
# =======================



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
    checkStudents = select(studentsTable).where(studentsTable.c["Program Code"] == programCode)
    if db_connection.execute(checkStudents).fetchone():
        raise PermissionError(f"There are still Students currently enrolled in {programCode}!\nPlease Edit or Unenroll them First.")

def constraint_enrolled_college(collegeCode):
    checkStudents = select(studentsTable).where(studentsTable.c["College Code"] == collegeCode)
    if db_connection.execute(checkStudents).fetchone():
        raise PermissionError(f"There are still Students currently enrolled in {collegeCode}!\nPlease Edit or Unenroll them First.") 
    
# =======================
#      CHECK REMOVE
# =======================


# =======================
#      CHECK DUPES
# =======================

def validate_studentduplicates(studentID):
    check = select(studentsTable).where(studentsTable.c["ID Number"] == studentID)
    if db_connection.execute(check).fetchone():
        raise ValueError(f"Student with ID Number {studentID} already exists!")

def validate_programduplicates(programCode):
    check = select(programsTable).where(programsTable.c["Program Code"] == programCode)
    if db_connection.execute(check).fetchone():
        raise ValueError(f"Program with Code {programCode} already exists!")
    
def validate_collegeduplicates(collegeCode):
    check = select(collegesTable).where(collegesTable.c["College Code"] == collegeCode)
    if db_connection.execute(check).fetchone():
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