from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = 'tbl_users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))

class Post(Base):
    __tablename__ = 'tbl_posts'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(100), index=True)
    email = Column(String(100), index=True)