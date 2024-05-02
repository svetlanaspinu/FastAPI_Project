        # hold the utilities functions
# sa ascundem parola userului in pgadmin tabel am run pip install passlib[bcrypt]
from passlib.context import CryptContext
# telling passlib the hashing algorithm, here-bcrypt
pwd_context = CryptContext(schemas=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)
# to hash a password we just have to call the hash
def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)