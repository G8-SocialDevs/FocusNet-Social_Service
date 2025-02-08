from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.publication import Publication
from app.schemas.publication import PublicationCreate, PublicationResponse, PublicationListResponse
from typing import List

router = APIRouter()

@router.post("/users/{user_id}/create_publication/", response_model=PublicationResponse)
def create_publication(user_id: int, publication: PublicationCreate, db: Session = Depends(get_db)):
    new_publication = Publication(
        ContentPubli=publication.ContentPubli,
        ImagePubli=publication.ImagePubli,
        UserID=user_id
    )
    db.add(new_publication)
    db.commit()
    db.refresh(new_publication)
    return {"PublicationID": new_publication.PublicationID, "message": "Publicación creada exitosamente"}


@router.get("/get_publications/", response_model=List[PublicationListResponse])
def list_all_publications(db: Session = Depends(get_db)):
    return db.query(Publication).all()