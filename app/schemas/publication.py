from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

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