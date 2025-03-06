from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional,List

class PublicationCreate(BaseModel):
    ContentPubli: str = Field(..., max_length=1000)
    ImagePubli: Optional[str] = Field(None, max_length=500)

class PublicationResponse(BaseModel):
    PublicationID: int
    message: str = "Publicación creada exitosamente"

class PublicationListResponse(BaseModel):
    PublicationID: int
    ContentPubli: str
    ImagePubli: Optional[str]
    Date: datetime
    UserID: int

class PublicationListResponseExtended(BaseModel):
    PublicationID: int
    ContentPubli: str
    ImagePubli: Optional[str]
    Date: datetime
    UserID: int
    CommentCount: int
    ReactionCount: int

class UserBasicResponse(BaseModel):
    UserID: int
    UserName: str
    UserImage: Optional[str]

class CommentResponseExtended(BaseModel):
    ContentComment: str
    Date: datetime
    User: UserBasicResponse

class DetailPublicationResponse(BaseModel):
    PublicationID: int
    ContentPubli: str
    ImagePubli: Optional[str]
    Date: datetime
    UserID: int
    CommentCount: int
    ReactionCount: int
    Reactions: List[UserBasicResponse] = []
    Comments: List[CommentResponseExtended] = []

class ProfileResponseExtended(BaseModel):
    UserID: int
    FirstName: str
    LastName: str
    UserName: str
    UserImage: Optional[str]
    Bio: Optional[str]
    PhoneNumber: Optional[str]
    PublicationCount: int
    ReactionCount: int