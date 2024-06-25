from pydantic import BaseModel, EmailStr
from typing import Union

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None

class Login(BaseModel):
    email: EmailStr
    password: str

class AddPost(BaseModel):
    id: int
    # email: str

class Post(BaseModel):
    id: int
    file_name: str
