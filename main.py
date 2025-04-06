import pymysql

mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="studentdbms",
    connect_timeout=5
)

