
from pydantic import BaseModel, EmailStr,Field
from datetime import datetime
from typing import Optional
from typing import Literal
from pydantic.types import conint


# class post(BaseModel):
#     title: str
#     content: str
#     published: bool= True


# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool= True

# class UpdatePost(BaseModel):
# #we might only want user to access the published field not any other chnages 

#     published: bool


#postbase handles the direction of the user sending data to us
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
        extra = "ignore"


class PostBase(BaseModel):
    title: str
    content: str
    published: bool= True

class PostCreate(PostBase):#here we are basically inheriting the title and content fields form the postbase
    pass

#post: us sending data to the user: response

class Post(PostBase):
    id: int
    owner_id:int
    created_at: datetime
    owner:UserOut
    class Config:
        from_attributes=True

class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        from_attributes=True



class Usercreate(BaseModel):
    email: EmailStr
    password:str






#security:-we'll need to hash the passwords and for that we'll need two libraries -passlib which willl handle the hashing and specifiy the algorithm bcrypt


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # id:int
    id:Optional[str]=None



class Vote(BaseModel):
    post_id: int
    dir: int = Field(ge=0, le=1)