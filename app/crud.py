from sqlalchemy.orm import Session

from .model import models
from .model import schemas
from .auth import pwd_context, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def add_post(db: Session, file_name: str, email: str):
    db_post = models.Post(file_name=file_name, email=email)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, email: str, skip: int = 0, limit: int = 10):
    # return db.query(models.Post).filter(models.Post.email == email).offset(skip).limit(limit).all()
    return db.query(models.Post).filter(models.Post.email == email).all()

def delete_post(db: Session, id: int):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not db_post:
        return False
    db.delete(db_post)
    db.commit()
    return db_post