from fastapi import FastAPI
# pt a face request din web browser
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


# dupa ce instalam Alembic nu mai avem nevoie de comanda de jos. pt ca tabelul este creat prin Alembic
#models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app = FastAPI()
# eplicatie 11h 20'
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# grabbing the router to include the specific routes in the post and user file
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}




