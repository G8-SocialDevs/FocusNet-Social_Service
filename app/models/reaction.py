from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class Reaction(Base):
    __tablename__ = "Reaction"
    
    ReactionID = Column(Integer, primary_key=True, autoincrement=True)
    PublicationID = Column(Integer, ForeignKey("Publication.PublicationID"), nullable=False)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    
    publication = relationship("Publication", back_populates="reactions")
    user = relationship("User", back_populates="reactions")