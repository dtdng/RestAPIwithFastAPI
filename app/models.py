from email.policy import default
from sqlalchemy import Column, Integer, String
from database import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    
    
class User(Base):
    __tablename__ = "user" 
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    password_hashed = Column(String)