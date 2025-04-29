from tkinter import messagebox
import re
from DATA import GlobalSQL

connection = GlobalSQL.return_connection()
cursor = connection.cursor()

# =======================
# ACCEPTED ENTRY FORMATS
# =======================
NormalEntry = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$")
ProgramEntry = re.compile(r"^Bachelor (of|Of) [A-Za-z\s\&\(\)]+$")
CollegeEntry = re.compile(r"^College (of|Of) [A-Za-z\s\&\(\)]+$")
IDEntry = re.compile(r"^\d{4}-\d{4}$")
EmailEntry = re.compile(r"^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}$")
CodeEntry = re.compile(r"^[A-Za-z]{3,12}$")
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
    
def check_count(query, value, error_message):
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    count = result[0] if isinstance(result, tuple) else result.get("COUNT(*)", 0)
    if count:
        raise PermissionError(error_message)

def constraint_enrolled_program(programCode):
    check_count(
        "SELECT COUNT(*) FROM students WHERE `Program Code` = %s",
        programCode,
        f"There are still Students currently enrolled in {programCode}!\nPlease Edit or Unenroll them First."
    )

def constraint_enrolled_college(collegeCode):
    check_count(
        "SELECT COUNT(*) FROM students WHERE `College Code` = %s",
        collegeCode,
        f"There are still Students currently enrolled in {collegeCode}!\nPlease Edit or Unenroll them First."
    )

def constraint_made_programs(collegeCode):
    check_count(
        "SELECT COUNT(*) FROM programs WHERE `College Code` = %s",
        collegeCode,
        f"There are still Programs currently under {collegeCode}!\nPlease Edit or Remove them First."
    )

# =======================
#      CHECK REMOVE
# =======================


# =======================
#      CHECK DUPES
# =======================

def validate_studentduplicates(id_number, edit=False, current_id=None):
    conn = GlobalSQL.return_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT `ID Number` FROM students WHERE `ID Number` = %s",
                (id_number,)
            )
            row = cursor.fetchone()
    finally:
        conn.close()

    if row:
        existing_id = row.get("ID Number")
        if edit and existing_id == current_id:
            return
        raise ValueError(f"Student with ID Number {id_number} already exists!")   

def validate_programduplicates(programCode, edit = False, current_pcode = None):

    conn = GlobalSQL.return_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT `Program Code` FROM programs WHERE `Program Code` = %s",
                (programCode,)
            )
            row = cursor.fetchone()
    finally:
        conn.close()

    if row:
        existing_id = row.get("ID Number")
        if edit and existing_id == current_pcode:
            return
        raise ValueError(f"Program with Code {programCode} already exists!")  
    
def validate_collegeduplicates(collegeCode, edit = False, current_ccode = None):

    conn = GlobalSQL.return_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT `College Code` FROM colleges WHERE `College Code` = %s",
                (collegeCode,)
            )
            row = cursor.fetchone()
    finally:
        conn.close()

    if row:
        existing_id = row.get("College Code")
        if edit and existing_id == current_ccode:
            return
        raise ValueError(f"College with Code {collegeCode} already exists!")

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