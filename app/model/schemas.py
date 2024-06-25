from pydantic import BaseModel, EmailStr

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

class Login(BaseModel):
    email: EmailStr
    password: str

class AddPost(BaseModel):
    id: int
    file_name: str
