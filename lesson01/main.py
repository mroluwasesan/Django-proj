from typing import Optional, Union
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    publish :bool = True
    ratings : Optional[int] = None
    
my_post = [{"title": "the US cars", "content": "most famous cars in the US", "id":1 },{"title": "US meals", "content":"this are the most common US foods", "id": 2}]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_post():
    return {"data":my_post}

@app.post("/createposts")
def createposts(post:post):
    post_dict = post.model_dump
    post.append()
    return {"date":post}