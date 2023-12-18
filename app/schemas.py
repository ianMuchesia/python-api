from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic.networks import EmailStr



    
class PostBase(BaseModel):
    title: str
    content:str
    published:bool=True
    rating:Optional[int] = None
    
class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: Optional[str] = None