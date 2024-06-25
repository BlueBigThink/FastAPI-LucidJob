from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated
import uuid
import os

from .model import models, schemas, database
from . import crud, auth

models.Base.metadata.create_all(bind=database.engine)

UPLOAD_FILE_MAX_SIZE = 1024 * 1024 * 1
UPLOAD_DIR = "./uploads"

app = FastAPI()

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/signup", response_model=schemas.Token)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = crud.create_user(db=db, user=user)
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return { "access_token": access_token,  "token_type": "bearer" }

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.Login, db: Session = Depends(database.get_db)):
    db_user = crud.authenticate_user(db=db, email=user.email, password=user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return { "access_token": access_token,  "token_type": "bearer" }

@app.post("/post", response_model=schemas.AddPost)
async def add_post(token_data: Annotated[schemas.TokenData, Depends(auth.get_token_data)], file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # check file size
    contents = await file.read()
    if len(contents) > UPLOAD_FILE_MAX_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 1MB limit")
    
    #save the file
    file_id = uuid.uuid4()
    file_name = f"{file_id}.txt"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(contents)
    
    #add the post
    post = crud.add_post(db=db, file_name=f"{file_id}", email=token_data.email)

    # store in memory

    return { "id" : post.id }

@app.get("/post", response_model=list[schemas.Post])
def get_post(token_data: Annotated[schemas.TokenData, Depends(auth.get_token_data)], db: Session = Depends(database.get_db)):
    posts = crud.get_post(db=db, email=token_data.email)
    # store in memory

    return posts

@app.delete("/post/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, token_data: Annotated[schemas.TokenData, Depends(auth.get_token_data)], db: Session = Depends(database.get_db)):
    post = crud.delete_post(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # store in memory

    return post
