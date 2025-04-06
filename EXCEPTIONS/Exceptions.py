from tkinter import messagebox
from DATA import GlobalHash, GlobalDFs
import re



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
    
def validate_programremove(removekey):
    if GlobalHash.showEnrolled(removekey):
        raise PermissionError("There are still Students currently enrolled!\nPlease Edit or Unenroll them First.")   

def validate_collegeremove(removekey):
    if GlobalHash.showConstituents(removekey):
        raise PermissionError("There are still Students currently enrolled!\nPlease Edit or Unenroll them First.")   
    
def validate_studentduplicates(duplicatekey, edit=False, currentstudent=None):
    Students = GlobalDFs.readStudentsDF()
    
    if edit and currentstudent:  
        students_tovalidatedupe = Students[Students['ID Number'] != currentstudent]
    else:
        students_tovalidatedupe = Students

    if (students_tovalidatedupe['ID'] == duplicatekey).sum() > 0:
        raise FileExistsError(f"Student with ID {duplicatekey} already exists!")


def validate_programduplicates(duplicatekey, edit=False, currentprogram=None):
    Programs = GlobalDFs.readProgramsDF()

    if edit and currentprogram:
        programs_tovalidatedupe = Programs[Programs['Program Code'] != currentprogram]
    else:
        programs_tovalidatedupe = Programs

    if (programs_tovalidatedupe['Program Code'] == duplicatekey).sum() > 0:
        raise FileExistsError(f"Program with code {duplicatekey} already exists!")
    
def validate_collegeduplicates(duplicatekey, edit=False, currentcollege=None):
    Colleges = GlobalDFs.readCollegesDF()

    if edit and currentcollege:
        colleges_tovalidatedupe = Colleges[Colleges['College Code'] != currentcollege]
    else:
        colleges_tovalidatedupe = Colleges
        
    if ((colleges_tovalidatedupe['College Code'] == duplicatekey).sum() > 0):
        raise FileExistsError(f"College with code {duplicatekey} already exists!")

# =======================
#      CHECK INPUTS
# =======================



# =======================
#     SHOW FUNCTIONS
# =======================
def show_removeerror_message(error):
    messagebox.showerror("Remove Error", str(error))

def show_duplicateerror_message(error):
    messagebox.showerror("Entity already exists!", str(error))

def show_inputerror_message(error):
    messagebox.showerror("Input Error", str(error))

def show_unexpected_error(error):
    messagebox.showerror("Unexpected Error", f"An error occurred: {str(error)}")
# =======================
#     SHOW FUNCTIONS
# =======================