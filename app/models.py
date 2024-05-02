# creating the tables in PgAdmin

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # to create columns
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
class Post(Base):
    __tablename__ = "posts" #tabel name

    # columns name
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default ='True', nullable=False )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
# generating tables with all the properties thru sqlalchemy
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

# this tells sqlalchemy to fetch some information based on the relationship
    owner = relationship("User")

#creating the user table in PgAdmin
class User(Base):
    __tablename__ = "users" # tabel name
    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



# model for the votes table
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
