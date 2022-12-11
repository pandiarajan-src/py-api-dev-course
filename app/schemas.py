from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    rating: int
    created_at: datetime
    
    class Config:
        orm_mode = True