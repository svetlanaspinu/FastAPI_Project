# moving the database code for testing from test_users.py ==here

from fastapi.testclient import TestClient # e de pe site-ul https://fastapi.tiangolo.com/tutorial/testing/
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app # importing the app instance
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# creating the tables in pgadmin for testing
#Base.metadata.create_all(bind=engine)


#def override_get_db():
    #db = TestingSessionLocal()
    #try:
       # yield db
   # finally:
       # db.close()


@pytest.fixture()  # sa ma interesez ce SCOPE face!!!!
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db # to yield = te return
    finally:
        db.close()




# setting our test-client to a variable called client
#client = TestClient(app) # am facut remove dupa ce am creat def client, pt return accease functie

# creating a fixture to remove the table violations constrains
@pytest.fixture()
def client(session): # passing seesion = because before to output the client fixture- the client will call the session before runs and this will create and drop the table
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    #Base.metadata.create_all(bind=engine)
# run the code before we run our test
    yield TestClient(app) # yield gives more flexibility; yield = return; # run our code after our test finishes
# drop the table after test finishes
    #Base.metadata.drop_all(bind=engine)