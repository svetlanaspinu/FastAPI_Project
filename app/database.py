# this file handel all the database connection

# toate acestea de pe fastapi sqlalchemy site
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"



engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency : https://fastapi.tiangolo.com/tutorial/sql-databases/
# get connection to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# connecting to PgAdmin using psycopg2 ---dupa nu am mai folodit ca am folodiy Postegre(PgAdmin)
#while True:
   # try:
        #conn = psycopg2.connect(host="localhost", database="FastAPI_Project", user="postgres", password="password456", cursor_factory=RealDictCursor)
    # to execute SQL statements
       # cursor = conn.cursor()
       # print("Database was successfull connected!")
        #break
   # except Exception as error:
       # print("Connecting to database failed!")
       # print("The error was ", error)
       #time.sleep(2)
