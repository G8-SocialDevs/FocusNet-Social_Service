from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Comment(Base):
    __tablename__ = "Comment"
    
    CommentID = Column(Integer, primary_key=True, autoincrement=True)
    ContentComment = Column(Text, nullable=False)
    PublicationID = Column(Integer, ForeignKey("Publication.PublicationID"), nullable=False)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    Date = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    
    publication = relationship("Publication", back_populates="comments")
    user = relationship("User", back_populates="comments")