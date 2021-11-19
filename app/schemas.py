from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from app.database import Base


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserData(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

# create base table model


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# schemas yang digunakan untuk memastikan kolom apa saja yang harus diinput
# berdasarkan base model diatas
class PostCreate(PostBase):
    pass


# menampilkan kolom yang akan dimunculkan di response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserData

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
