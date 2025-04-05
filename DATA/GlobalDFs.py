import pandas as pd
from sqlalchemy import create_engine

def readStudents():
    db_connection_str = 'mysql+pymysql://root:root@localhost/studentdbms'
    db_connection = create_engine(db_connection_str)

    df = pd.read_sql('SELECT * FROM students', con=db_connection)

    return df





# #==================
# # READING FUNCTIONS
# #==================
# def readStudentsDF():
#     Students = pd.read_csv(r'DATA\Students.csv')
#     StudentsDF = pd.DataFrame(Students)
#     # print(StudentsDF)
#     return StudentsDF
 
# def readProgramsDF():
#     Programs = pd.read_csv(r'DATA\Programs.csv')
#     ProgramsDF = pd.DataFrame(Programs)
#     # print(ProgramsDF)
#     return ProgramsDF

# def readCollegesDF():
#     Colleges = pd.read_csv(r'DATA\Colleges.csv')
#     CollegesDF = pd.DataFrame(Colleges)
#     # print(CollegesDF)
#     return CollegesDF
# #==================
# # READING FUNCTIONS
# #==================



# #==================
# # UPDATE FUNCTIONS
# #==================
# def updateDF(dataframe):
    
#     match(dataframe.columns[0]):
#             case(r"ID"):
#                 newdataframe = readStudentsDF()

#             case(r"Program Code"):
#                 newdataframe = readProgramsDF()

#             case(r"College Code"):
#                 newdataframe = readCollegesDF()
    
#     return newdataframe
# #==================
# # UPDATE FUNCTIONS
# #==================



# #==================
# # WRITING FUNCTIONS
# #==================
# def writeStudentsDF(newStudentdf):

#     newStudentdf.to_csv('DATA/Students.csv', mode='w', header=True, index=False)

# def writeProgramsDF(newProgramdf):

#     newProgramdf.to_csv('DATA/Programs.csv', mode='w', header=True, index=False)

# def writeCollegesDF(newCollegedf):

#     newCollegedf.to_csv('DATA/Colleges.csv', mode='w', header=True, index=False)
# #==================
# # WRITING FUNCTIONS
# #==================



# #==================
# # APPENDING FUNCTIONS
# #==================
# def appendStudentsDF(newStudentdf):
#     studentsDF = readStudentsDF()

#     # Append only if the ID does not already exist
#     studentsDF = pd.concat([studentsDF, newStudentdf]).drop_duplicates(subset=["ID"], keep="last")

#     # Save back to CSV
#     writeStudentsDF(studentsDF)

      
# def appendProgramsDF(newProgramdf):
#     programsDF = readProgramsDF()

#     # Append only if the ID does not already exist
#     programsDF = pd.concat([programsDF, newProgramdf]).drop_duplicates(subset=["Program Code"], keep="last")

#     # Save back to CSV
#     writeProgramsDF(programsDF)

# def appendCollegesDF(newCollegedf):
#     collegesDF = readCollegesDF()

#     # Append only if the ID does not already exist
#     collegesDF = pd.concat([collegesDF, newCollegedf]).drop_duplicates(subset=["College Code"], keep="last")

#     # Save back to CSV
#     writeProgramsDF(collegesDF)
# #==================
# # APPENDING FUNCTIONS
# #==================