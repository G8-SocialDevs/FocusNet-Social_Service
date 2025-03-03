from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse
from typing import List

router = APIRouter()

@router.post("/users/{user_id}/publications/{publication_id}/create_comment/", response_model=CommentResponse)
def create_comment(user_id: int, publication_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    new_comment = Comment(
        ContentComment=comment.ContentComment,
        PublicationID=publication_id,
        UserID=user_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.delete("/delete_comment/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.CommentID == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    db.delete(comment)
    db.commit()
    return {"message": "Comentario eliminado exitosamente"}

@router.get("/publications/{publication_id}/list_publication_comments/", response_model=List[CommentResponse])
def list_publication_comments(publication_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.PublicationID == publication_id).all()