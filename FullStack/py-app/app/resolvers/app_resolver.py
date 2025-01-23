from fastapi import HTTPException
from sqlmodel import Session
import strawberry
from typing import List
from app.models.post import Post, User
from app.db import engine

@strawberry.type
class PostType:
    id: int
    title: str
    content: str

@strawberry.type
class UserType:
    id: int
    username: str
    email: str
    posts: List[PostType]

@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, id: int) -> UserType:
        with Session(engine) as session:
            user = session.get(User, id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return UserType(id=user.id, username=user.username, email=user.email, posts=user.posts)
    
    @strawberry.field
    def get_post(self, id: int) -> PostType:
        with Session(engine) as session:
            post = session.get(Post, id)
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            return PostType(id=post.id, title=post.title, content=post.content)
        
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, username: str, email: str) -> UserType:
        with Session(engine) as session:
            new_user = User(username=username, email=email)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return UserType(id=new_user.id, username=new_user.username, email=new_user.email, posts=[])
        
    @strawberry.mutation
    def create_post(self, title: str, content: str, author_id: int) -> PostType:
        with Session(engine) as session:
            new_post = Post(title=title, content=content, author_id=author_id)
            session.add(new_post)
            session.commit()
            session.refresh(new_post)
            return PostType(id=new_post.id, title=new_post.title, content=new_post.content)

schema = strawberry.Schema(query=Query, mutation=Mutation)