from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hello duniaku"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}


@app.post("/posts")
def create_post(new_post: Post):
    print(new_post)
    return {"data": new_post}
