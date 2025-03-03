from pydantic import BaseModel

class ReactionCreate(BaseModel):
    pass 

class ReactionResponse(BaseModel):
    ReactionID: int
    PublicationID: int
    UserID: int
