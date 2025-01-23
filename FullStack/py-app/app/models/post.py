from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.db import engine

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int = Field(default=None, foreign_key="user.id")

    author: "User" = Relationship(back_populates="posts")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str

    posts: List[Post] = Relationship(back_populates="author")

SQLModel.metadata.create_all(engine)