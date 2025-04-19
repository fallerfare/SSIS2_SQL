from sqlalchemy import create_engine, update, Column, ForeignKey, ForeignKeyConstraint, VARCHAR, or_, desc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd


#==================
#  SETUP DATAFRAME
#==================
Base = declarative_base()

class Students(Base):
    __tablename__ = "students"

    id = Column("ID Number", VARCHAR(50), primary_key = True)
    fn = Column("First Name", VARCHAR(50))
    ln = Column("Last Name", VARCHAR(50))
    em = Column("Email", VARCHAR(100))
    yl = Column("Year Level", VARCHAR(20))
    gn = Column("Gender", VARCHAR(15))
    pC = Column("Program Code", VARCHAR(15))
    cC = Column("College Code", VARCHAR(15))

    __table_args__ = (
        ForeignKeyConstraint(
            ["Program Code"], ["programs.Program Code"],
            ondelete="RESTRICT"
        ),
        ForeignKeyConstraint(
            ["College Code"], ["colleges.College Code"],
            ondelete="RESTRICT"
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
            ondelete="RESTRICT"
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


db_connection_str       = 'mysql+pymysql://root:root@localhost/studentdbms'
engine                  = create_engine(db_connection_str, echo = True)

Base.metadata.create_all(bind = engine)
SessionLocal = sessionmaker(bind=engine)
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

def updateStudents(old_programCode, new_programCode):

    enrolledStudents = update(Students).where(
                    Students.pC == old_programCode).values(
                    Students.pC == new_programCode)
    session.execute(enrolledStudents).all()
    session.commit()

def updatePrograms(old_collegeCode, new_collegeCode):

    deptPrograms = update(Programs).where(
                    Programs.cC == old_collegeCode).values(
                    Programs.cC == new_collegeCode)
    session.execute(deptPrograms).all()
    session.commit()

def updateConstituents(old_collegeCode, new_collegeCode):

    constStudents = update(Students).where(
                    Students.cC == old_collegeCode).values(
                    Students.cC == new_collegeCode)
    session.execute(constStudents).all()
    session.commit()

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



#==================
# FILTER DATAFRAME
#==================

def filterDF(search_term=None, search_type=None, sort_with=None, sort_by="Ascending", tab=None):
    model_map = {
        "students": Students,
        "programs": Programs,
        "colleges": Colleges
    }
    model = model_map.get(tab.lower())
    if not model:
        return pd.DataFrame()

    base_query = session.query(model)
    filters = []

    # ============ 
    # FILTERING
    # ============
    if search_term:
        if search_type:  # Specific column
            col = next((c for c in model.__table__.columns if c.name == search_type), None)
            if col is not None:
                filters.append(col.like(f"%{search_term}%"))
        else:  # Search all string columns
            string_cols = [c for c in model.__table__.columns if isinstance(c.type, VARCHAR)]
            filters.extend([c.like(f"%{search_term}%") for c in string_cols])

    if filters:
        base_query = base_query.filter(or_(*filters))

    # ============ 
    # SORTING
    # ============
    sort_clause = None
    if sort_with:
        col = next((c for c in model.__table__.columns if c.name == sort_with), None)
        if col is not None:
            sort_clause = desc(col) if sort_by.lower() == "descending" else col

    if sort_clause is not None:
        base_query = base_query.order_by(sort_clause)

    # ============ 
    # EXECUTE 
    # ============
    results = base_query.all()
    if not results:
        return pd.DataFrame()

    df = pd.DataFrame([r.__dict__ for r in results])
    df.drop(columns=["_sa_instance_state"], inplace=True)

    return df

#==================
# FILTER DATAFRAME
#==================