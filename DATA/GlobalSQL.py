import pymysql
from pymysql import cursors
import pandas as pd
from DATA.db_config import DB_PASSWORD, DB_DATABASE, DB_HOST, DB_USER


#==================
#  SETUP DATAFRAME
# #==================
def return_connection():
    return pymysql.connect(
        host = f"{DB_HOST}",
        user = f"{DB_USER}",
        password = f"{DB_PASSWORD}",
        database = f"{DB_DATABASE}",
        cursorclass=cursors.DictCursor
    )

#==================
#  SETUP DATAFRAME
#==================


#==================
# READING FUNCTIONS
#==================

def returnDataframe(query, params = None):
    connection = return_connection()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return pd.DataFrame(result)

def readStudentsDF():
    students = "SELECT * FROM students"
    return returnDataframe(students)

def readProgramsDF():
    programs = "SELECT * FROM programs"
    return returnDataframe(programs)

def readCollegesDF():
    colleges = "SELECT * FROM colleges"
    return returnDataframe(colleges)

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