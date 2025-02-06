from typing import Optional, Union
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish :bool = True
    ratings : Optional[int] = None

while True:
    try:
        conn = psycopg.connect("host= localhost dbname= fastapi user=postgres password=admin port=5432", row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection successful")
        break

    except Exception as error:
        print(f"Database connection failed: {error}")
        time.sleep(5)
    
my_post = [{"title": "the US cars", "content": "most famous cars in the US", "id":1 },{"title": "US meals", "content":"this are the most common US foods", "id": 2}]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def createposts(post:Post):
    cursor.execute("""INSERT INTO posts (title, content, publish) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.publish))
    new_post = cursor.fetchone()
    conn.commit()
    return {"date":new_post}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    #post = find_post(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} was not found")
    print(post)
    return {"data":f"this is post number {id} containing title: {post["title"]}"}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    return {Response(status_code=status.HTTP_204_NO_CONTENT)}

@app.put("/posts/{id}")
def update_post(id:int, post:Post):    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, publish = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.publish, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    return {"data":updated_post}