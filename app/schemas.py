from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional,Literal


class UserCreate(BaseModel):
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
class PostCreate(PostBase):
    pass
class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None       
    published: Optional[bool] = None

class PostResponse(PostCreate):
    id: int
    created_at: datetime
    owner: "UserResponse"

    class Config:
        orm_mode = True
class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int      
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
    class config:
        orm_mode = True
class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]

    class Config:
        orm_mode = True
   
