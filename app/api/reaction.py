from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reaction import Reaction
from app.schemas.reaction import ReactionCreate, ReactionResponse
from typing import List

router = APIRouter()

@router.post("/users/{user_id}/publications/{publication_id}/reactions/", response_model=ReactionResponse)
def react_to_publication(user_id: int, publication_id: int, reaction: ReactionCreate, db: Session = Depends(get_db)):
    new_reaction = Reaction(
        PublicationID=publication_id,
        UserID=user_id
    )
    db.add(new_reaction)
    db.commit()
    db.refresh(new_reaction)
    return new_reaction

@router.delete("/users/{user_id}/publications/{publication_id}/reactions/")
def delete_reaction(user_id: int, publication_id: int, db: Session = Depends(get_db)):
    reaction = db.query(Reaction).filter(
        Reaction.PublicationID == publication_id,
        Reaction.UserID == user_id
    ).first()
    if not reaction:
        raise HTTPException(status_code=404, detail="Reacción no encontrada")
    db.delete(reaction)
    db.commit()
    return {"message": "Reacción eliminada exitosamente"}
