# contains path operations dealing with posts
from .. import models, schemas, oauth2
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func # for the count ti join the tables

router = APIRouter()     # in loc de /posts din decorator punem doar /-slashul


# getting all posts
@router.get("/posts", response_model=List[schemas.PostOut])
def get_posts(db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM public.posts""") # posts from Postman
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(seach)).limit(limit).offset(skip).all()
    
# facind JOIN -urole pt PGAdmin de aici/ == face joinurile
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(serach)).limit(limit).offset(skip).all()

    return posts


# creating a Post
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

# push the tabel changes to PgAdmin
    #conn.commit()
    # addind to the PgAdmin database
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)  # addind to the PgAdmin database
    db.commit()
    db.refresh(new_post)
    return new_post


# getting an individual post
@router.get('/posts/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # 1h 57m nu am HTTP output 

    return post


# DELETING A POST
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING* """, (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")


    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Post
@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, (str(id),)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()


    return post_query.first()