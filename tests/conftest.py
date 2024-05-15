# in this file i have defined all the fixtures. is a special file that pytest uses. any fixture defined here it will automatically be accesible 
# any other test within this packages. it's a package specific file.

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
from app.oauth2 import create_access_token


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


# fixture to creat a test user
@pytest.fixture
def test_user(client):  #make a call to creat userout accesing through client
    user_data = {"email": "hello123@gmail.com", "password": "password456"}
    res = client.post("/users/", json=user_data) # /users/ - we are sending the information to user table
    new_user = res.json()
    new_user["password"] = user_data['password']
# return the information about the user
    return new_user


@pytest.fixture
def token(test_user): #test_user din paranteza inseamna ca intii avem nevoie sa creeam userul si apoi accesam tokenul
    return create_access_token({"user_id": test_user['id']}) # in acolade inseamna ca e sub forma de dictionary


# fixture to authenticate the client
@pytest.fixture
def authorized_client(client, token):
    #update the client into the headers in postman probabil
    client.headers = { 
        **client.headers, # ** - call all the clients or the inputs
        "Authorization": f"Bearer {token}"
    }
    return client 
