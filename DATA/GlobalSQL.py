import pymysql
import pandas as pd
from DATA.db_config import DB_PASSWORD, DB_DATABASE, DB_HOST, DB_USER

#==================
#  SETUP DATAFRAME
# #==================

connection = pymysql.connect(
    host = f"{DB_HOST}",
    user = f"{DB_USER}",
    password = f"{DB_PASSWORD}",
    database = f"{DB_DATABASE}"
)

cursor = connection.cursor()

#==================
#  SETUP DATAFRAME
#==================


#==================
# READING FUNCTIONS
#==================

def readStudentsDF():
    students = "SELECT * FROM students"
    return pd.read_sql(students, con = connection)

def readProgramsDF():
    programs = "SELECT * FROM programs"
    return pd.read_sql(programs, con = connection)

def readCollegesDF():
    colleges = "SELECT * FROM colleges"
    return pd.read_sql(colleges, con = connection)

#==================
# READING FUNCTIONS
#==================



#==================
# UPDATE FUNCTIONS
#==================

def updateDF(dataframe):
    first_col = dataframe.columns[0]

    if "ID Number" in first_col:
        return readStudentsDF()
    elif "Program Code" in first_col:
        return readProgramsDF()
    elif "College Code" in first_col:
        return readCollegesDF()
    else:
        return dataframe  

#==================
# UPDATE FUNCTIONS
#==================