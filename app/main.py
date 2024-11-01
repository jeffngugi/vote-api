from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI() 




class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi', 
                                user='postgres',
                                password='password',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection was successful")
        break
    except Exception as error:
        print("DB connection failed")
        print("The error was", error)
        time.sleep(3)
    


@app.get("/")
def root():
    return {"message": "Hello World: from Jeff Ngugi"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
#    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
#                         (post.title, post.content, post.published) )
#    new_post = cursor.fetchone()
#    conn.commit()
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"CREATED": new_post}
      
    
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
    return {
        "post details": post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", (str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    print(post)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return {"data": 'post'}