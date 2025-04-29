from tkinter import messagebox
import re
from DATA import GlobalSQL
import pymysql

connection = GlobalSQL.connection()
cursor = GlobalSQL.cursor()

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
    checkStudents = f"SELECT COUNT(*) FROM students WHERE `Program Code` = {programCode}"
    cursor.execute(checkStudents)
    if cursor.fetchone()[0]:
        raise PermissionError(f"There are still Students currently enrolled in {programCode}!\nPlease Edit or Unenroll them First.")

def constraint_enrolled_college(collegeCode):
    checkStudents = f"SELECT COUNT(*) FROM students WHERE `College Code` = {collegeCode}"
    cursor.execute(checkStudents)
    if cursor.fetchone()[0]:
        raise PermissionError(f"There are still Students currently enrolled in {collegeCode}!\nPlease Edit or Unenroll them First.")
    
def constraint_made_programs(collegeCode):
    checkPrograms = f"SELECT COUNT(*) FROM programs WHERE `College Code` = {collegeCode}"
    cursor.execute(checkPrograms)
    if cursor.fetchone()[0]:
        raise PermissionError(f"There are still Programs currently under {collegeCode}!\nPlease Edit or Remove them First.")
    
# =======================
#      CHECK REMOVE
# =======================


# =======================
#      CHECK DUPES
# =======================

def validate_studentduplicates(studentID, edit = False, current_id = None):

    checkStudents = f"SELECT COUNT(*) FROM students WHERE `ID Number` = {studentID}"
    cursor.execute(checkStudents)
    if edit and cursor.fetchone()[0] and cursor == current_id:
        return
    elif not edit and cursor.fetchone()[0]:
        raise ValueError(f"Student with ID Number {studentID} already exists!")   

def validate_programduplicates(programCode, edit = False, current_pcode = None):
    
    checkPrograms = f"SELECT COUNT(*) FROM programs WHERE `Program Code` = {programCode}"
    cursor.execute(checkPrograms)
    if edit and cursor.fetchone()[0] and cursor == current_pcode:
        return
    elif not edit and cursor.fetchone()[0]:
        raise ValueError(f"Program with Code {programCode} already exists!")  
    
def validate_collegeduplicates(collegeCode, edit = False, current_ccode = None):
    
    checkPrograms = f"SELECT COUNT(*) FROM colleges WHERE `College Code` = {collegeCode}"
    cursor.execute(checkPrograms)
    if edit and cursor.fetchone()[0] and cursor == current_ccode:
        return
    elif not edit and cursor.fetchone()[0]:
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