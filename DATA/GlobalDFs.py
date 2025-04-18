import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, select, update

db_connection_str      = 'mysql+pymysql://root:root@localhost/studentdbms'
db_connection          = create_engine(db_connection_str).connect()
metadata               = MetaData()
collegesTable          = Table('colleges', metadata, autoload_with=db_connection)
programsTable          = Table('programs', metadata, autoload_with=db_connection)
studentsTable          = Table('students', metadata, autoload_with=db_connection)


#==================
# READING FUNCTIONS
#==================
def readStudentsDF():
   
    df = pd.read_sql('SELECT * FROM students', con=db_connection)

    return df

def readProgramsDF():
   
    df = pd.read_sql('SELECT * FROM programs', con=db_connection)

    return df

def readCollegesDF():
    
    df = pd.read_sql('SELECT * FROM colleges', con=db_connection)

    return df
#==================
# READING FUNCTIONS
#==================



#==================
# UPDATE FUNCTIONS
#==================

def updateStudents(old_programCode, new_programCode):

    enrolledStudents = update(studentsTable).where(
                    studentsTable.c["Program Code"] == old_programCode).values(
                    studentsTable.c["Program Code"] == new_programCode)
    db_connection.execute(enrolledStudents).all()

def updatePrograms(old_collegeCode, new_collegeCode):

    deptPrograms = update(programsTable).where(
                    programsTable.c["College Code"] == old_collegeCode).values(
                    programsTable.c["College Code"] == new_collegeCode)
    db_connection.execute(deptPrograms).all()

def updateConstituents(old_collegeCode, new_collegeCode):

    constStudents = update(studentsTable).where(
                    studentsTable.c["College Code"] == old_collegeCode).values(
                    studentsTable.c["College Code"] == new_collegeCode)
    db_connection.execute(constStudents).all()

#==================
# UPDATE FUNCTIONS
#==================



#==================
# UPDATE DATAFRAME
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
# UPDATE DATAFRAME
#==================