from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "User"
    
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String(50), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    FirstName = Column(String(25), nullable=False)
    LastName = Column(String(25), nullable=False)
    UserName = Column(String(25), unique=True, nullable=False)
    UserImage = Column(String(500))
    Bio = Column(Text)
    PhoneNumber = Column(String(9), unique=True)
    
    publications = relationship("Publication", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    reactions = relationship("Reaction", back_populates="user")