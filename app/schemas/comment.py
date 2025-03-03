from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    ContentComment: str = Field(..., max_length=1000)

class CommentResponse(BaseModel):
    CommentID: int
    ContentComment: str
    PublicationID: int
    UserID: int
    Date: datetime
