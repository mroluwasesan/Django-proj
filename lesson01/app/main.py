from typing import Optional, Union
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish :bool = True
    ratings : Optional[int] = None
    
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
    return {"data":my_post}

@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def createposts(post:Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0,1000)
    my_post.append(post_dict)
    return {"date":post_dict}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"message": f"post with id:{id} was not found"}
    print(post)
    return {"data":f"this is post number {id} containing title: {post["title"]}"}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index =find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    my_post.pop(index)
    return {Response(status_code=status.HTTP_204_NO_CONTENT)}

@app.put("/posts/{id}")
def update_post(id:int, post:Post):    
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_post[index] = post_dict
    return {"data":post_dict}