from typing import Union, List
from pydantic import BaseModel


class Student(BaseModel):
    name: str
    age: int
    class Config:
        orm_mode = True;
    

class StudentOutput(Student):
    name: str
    age: int
    class Config:
        orm_mode = True;
    
class StudentInDB(Student):
    password_hashed: str
    
    
class User(BaseModel):
    name: str
    username: str
    class Config:
        orm_mode = True;
        
        
class UserInput(User):
    password: str


class UserInDB(User):
    password_hashed: str
    
    
class LoginUser(BaseModel):
    username: str
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []