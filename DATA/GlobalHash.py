from DATA import GlobalDFs
from sqlalchemy import create_engine, Table, MetaData, select

db_connection_str      = 'mysql+pymysql://root:root@localhost/studentdbms'
db_connection          = create_engine(db_connection_str).connect()
metadata               = MetaData()
collegesTable          = Table('colleges', metadata, autoload_with=db_connection)
programsTable          = Table('programs', metadata, autoload_with=db_connection)
studentsTable          = Table('students', metadata, autoload_with=db_connection)

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

