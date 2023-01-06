from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime


# Request for User
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Response for User
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Request for User Login
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

# Request Base Model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool

# Request Create Model
class CreatePost(PostBase):
    rating: Optional[int] = None

class UpdatePost(CreatePost):
    pass

# Response Model
class Post(PostBase):
    id: int
    rating: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True


class PostResult(BaseModel):
    Posts: Post
    votes: int

    class Config:
        orm_mode = True

# Request for Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    post_dir: conint(le=1)


