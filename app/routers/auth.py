# holds the Authentication (JWT Tokens)

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter()



@router.post('/login', response_model=schemas.Token)
def login(user_credendials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credendials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    if not utils.verify(user_credendials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

# create a token 
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
# return token 
    return{"acess token": access_token, "token_type": "bearer" }
 
