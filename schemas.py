from pydantic import BaseModel, EmailStr
from typing import Optional

class Book(BaseModel):
    name:str
    author:str
    genre:Optional[str] = None
    publication: Optional[str] = None
    issued_by : Optional[int] =None

class User(BaseModel):
    name:str
    password:str
    age:int

class UserUpdate(BaseModel):
    name:Optional[str] =None
    age:Optional[int] =None

class UserCreate(BaseModel):
    name:str
    email: EmailStr
    password:str
    age:int
    id : str = None

class BookCreate(BaseModel):
    name:str
    author:str
    genre:Optional[str] = None
    publication: Optional[str] = None
    #issued_by : Optional[int] =None


class Token(BaseModel):
    access_token: str
    token_type: str