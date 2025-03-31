from DATA import GlobalDFs

def StudentHash(dataframe):
    dataframe = dataframe.drop_duplicates(subset=["ID"])
    return dataframe.set_index("ID").to_dict(orient="index")

def ProgramsHash(dataframe):
    dataframe = dataframe.drop_duplicates(subset=["Program Code"])
    return dataframe.set_index("Program Code").to_dict(orient="index")

def CollegesHash(dataframe):
    dataframe = dataframe.drop_duplicates(subset=["College Code"])
    return dataframe.set_index("College Code").to_dict(orient="index")

def showEnrolled(programcode):
    Students = StudentHash(GlobalDFs.readStudentsDF())
    EnrolledStudents = []
    for student_id in Students:
        student_info = Students[student_id]
        if student_info["Program Code"] == programcode:
            EnrolledStudents.append(student_id)
    return EnrolledStudents

def showDegrees(collegecode):
    Programs = ProgramsHash(GlobalDFs.readProgramsDF())
    EstablishedDegrees = []
    for program_code in Programs:
        program_info = Programs[program_code]
        if program_info["College Code"] == collegecode:
            EstablishedDegrees.append(program_code)
    return EstablishedDegrees

def showConstituents(collegecode):
    Constituents = []
    for program in showDegrees(collegecode):
        Constituents.append(showEnrolled(program))
    return Constituents

def updateStudents(oldprogramcode, programcode):
    Students = GlobalDFs.readStudentsDF()
    Students.loc[Students["Program Code"] == oldprogramcode, "Program Code"] = programcode
    GlobalDFs.writeStudentsDF(Students)  

def updateConstituents(oldcollegecode, collegecode):
    Students = GlobalDFs.readStudentsDF()
    Students.loc[Students["College Code"] == oldcollegecode, "College Code"] = collegecode
    GlobalDFs.writeStudentsDF(Students)  

def updatePrograms(oldcollegecode, collegecode):
    Programs = GlobalDFs.readProgramsDF()
    Programs.loc[Programs["College Code"] == oldcollegecode, "College Code"] = collegecode
    GlobalDFs.writeProgramsDF(Programs)

