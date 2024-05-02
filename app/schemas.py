from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# column from the PgAdmin table
class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass

# to hide user password in postman(sa nu fie arata passwordul)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True


# response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

# to transfrom the text in pydentic model(sa nu fie citit ca list, dar sa fie acceptat ca orice model)
    class Config:
        orm_mode = True

#
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

# creating the schemas for user
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

 # the schema for the Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


# schema for voting
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
