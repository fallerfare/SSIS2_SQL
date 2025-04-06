import pandas as pd
from sqlalchemy import create_engine

#==================
# READING FUNCTIONS
#==================
def readStudentsDF():
    db_connection_str = 'mysql+pymysql://root:root@localhost/studentdbms'
    db_connection = create_engine(db_connection_str)

    df = pd.read_sql('SELECT * FROM students', con=db_connection)

    return df

def readProgramsDF():
    db_connection_str = 'mysql+pymysql://root:root@localhost/studentdbms'
    db_connection = create_engine(db_connection_str)

    df = pd.read_sql('SELECT * FROM programs', con=db_connection)

    return df

def readCollegesDF():
    db_connection_str = 'mysql+pymysql://root:root@localhost/studentdbms'
    db_connection = create_engine(db_connection_str)

    df = pd.read_sql('SELECT * FROM colleges', con=db_connection)

    return df
#==================
# READING FUNCTIONS
#==================



#==================
# UPDATE FUNCTIONS
#==================
def updateDF(dataframe):
    
    match(dataframe.columns[0]):
            case(r"ID Number"):
                newdataframe = readStudentsDF()

            case(r"Program Code"):
                newdataframe = readProgramsDF()

            case(r"College Code"):
                newdataframe = readCollegesDF()
    
    return newdataframe
#==================
# UPDATE FUNCTIONS
#==================



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