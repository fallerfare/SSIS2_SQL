from sqlalchemy import create_engine, update, Column, ForeignKeyConstraint, VARCHAR, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd


#==================
#  SETUP DATAFRAME
#==================
Base = declarative_base()

class Students(Base):
    __tablename__ = "students"

    id = Column("ID Number",    VARCHAR(50), primary_key = True)
    fn = Column("First Name",   VARCHAR(50))
    ln = Column("Last Name",    VARCHAR(50))
    em = Column("Email",        VARCHAR(100))
    yl = Column("Year Level",   VARCHAR(20))
    gn = Column("Gender",       VARCHAR(15))
    pC = Column("Program Code", VARCHAR(15))
    cC = Column("College Code", VARCHAR(15))

    __table_args__ = (
        ForeignKeyConstraint(
            ["Program Code"], ["programs.Program Code"],
            ondelete="RESTRICT",
            onupdate="CASCADE"
        ),
        ForeignKeyConstraint(
            ["College Code"], ["colleges.College Code"],
            ondelete="RESTRICT",
            onupdate="CASCADE"
        ),
    )

    def __init__(self, id, fn, ln, em, yl, gn, pC, cC):
        self.id = id
        self.fn = fn
        self.ln = ln
        self.em = em
        self.yl = yl
        self.gn = gn
        self.pC = pC
        self.cC = cC

    def __repr__(self):
        return f"({self.id}, {self.fn}, {self.ln}, {self.em}, {self.yl}, {self.gn}, {self.pC}, {self.cC})"
    
class Programs(Base):
    __tablename__ = "programs"

    pC = Column("Program Code", VARCHAR(15), primary_key = True)
    pn = Column("Program Name", VARCHAR(50))
    cC = Column("College Code", VARCHAR(15))

    __table_args__ = (
        ForeignKeyConstraint(
            ["College Code"], ["colleges.College Code"],
            ondelete="RESTRICT",
            onupdate="CASCADE"
        ),
    )

    def __init__(self, pC, pn, cC):
        self.pC = pC
        self.pn = pn
        self.cC = cC

    def __repr__(self):
        return f"({self.pC}, {self.pn}, {self.cC})"
    
class Colleges(Base):
    __tablename__ = "colleges"

    cC = Column("College Code", VARCHAR(15), primary_key = True)
    cn = Column("College Name", VARCHAR(50))

    def __init__(self, cC, cn):
        self.cC = cC
        self.cn = cn

    def __repr__(self):
        return f"({self.cC}, {self.cn})"


db_connection_str       = 'mysql+pymysql://root:root@localhost/teststudentdbms'
engine                  = create_engine(db_connection_str, echo = True)
connection              = engine.connect()


Base.metadata.create_all(bind = engine)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)

studentsTable = metadata.tables["students"]
programsTable = metadata.tables["programs"]
collegesTable = metadata.tables["colleges"]
session = SessionLocal()

#==================
#  SETUP DATAFRAME
#==================


#==================
# READING FUNCTIONS
#==================

def readStudentsDF():
    return pd.read_sql_table("students", con = engine)

def readProgramsDF():
    return pd.read_sql_table("programs", con = engine)

def readCollegesDF():
    return pd.read_sql_table("colleges", con = engine)

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