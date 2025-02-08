from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user import User
from app.models.comment import Comment
from app.models.reaction import Reaction

class Publication(Base):
    __tablename__ = "Publication"
    
    PublicationID = Column(Integer, primary_key=True, autoincrement=True)
    ContentPubli = Column(Text, nullable=False)
    ImagePubli = Column(String(500))
    Date = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    
    user = relationship("User", back_populates="publications")
    comments = relationship("Comment", back_populates="publication")
    reactions = relationship("Reaction", back_populates="publication")