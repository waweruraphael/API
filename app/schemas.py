
from typing import Optional
from pydantic import BaseModel,EmailStr, conint
from datetime import datetime
from app.oauth import access_token




class PostBase(BaseModel):
    title:str
    content:str
    published :bool = True
   

class PostCreate(PostBase):
    pass  

class Post(PostBase):
    id:str
    created_at:datetime
    user_id :int

    class Config:
        orm_mode = True

class PostVote(BaseModel):
    Post : Post
    votes :int
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email:EmailStr
    password :str  


class UserOut(BaseModel):
    id :int
    email:EmailStr

    class Config:
        orm_mode = True

#user login credentials

class UserLogin(BaseModel) :
    email:EmailStr
    password:str    

class Token(BaseModel):
    access_token :str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None               


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
