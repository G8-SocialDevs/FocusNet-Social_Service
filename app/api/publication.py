from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.publication import Publication
from app.models.comment import Comment
from app.models.reaction import Reaction
from app.models.user import User
from app.schemas.publication import PublicationCreate, PublicationResponse, PublicationListResponse, PublicationListResponseExtended, UserBasicResponse, CommentResponseExtended, DetailPublicationResponse
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

@router.get("/list_publications/", response_model=List[PublicationListResponseExtended])
def list_publications(db: Session = Depends(get_db)):
    publications = (
        db.query(
            Publication,
            func.count(Comment.CommentID).label("CommentCount"),
            func.count(Reaction.ReactionID).label("ReactionCount"),
        )
        .outerjoin(Comment, Publication.PublicationID == Comment.PublicationID)
        .outerjoin(Reaction, Publication.PublicationID == Reaction.PublicationID)
        .group_by(Publication.PublicationID)
        .all()
    )
    
    return [
        {
            "PublicationID": pub.PublicationID,
            "ContentPubli": pub.ContentPubli,
            "ImagePubli": pub.ImagePubli,
            "Date": pub.Date,
            "UserID": pub.UserID,
            "CommentCount": comment_count,
            "ReactionCount": reaction_count
        }
        for pub, comment_count, reaction_count in publications
    ]

@router.get("/obtain_publication/{publication_id}", response_model=DetailPublicationResponse)
def obtain_publication(publication_id: int, db: Session = Depends(get_db)):
    publication = (
        db.query(
            Publication,
            func.count(Comment.CommentID).label("CommentCount"),
            func.count(Reaction.ReactionID).label("ReactionCount")
        )
        .outerjoin(Comment, Publication.PublicationID == Comment.PublicationID)
        .outerjoin(Reaction, Publication.PublicationID == Reaction.PublicationID)
        .filter(Publication.PublicationID == publication_id)
        .group_by(Publication.PublicationID)
        .first()
    )
    
    if not publication:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    
    pub, comment_count, reaction_count = publication
    
    reactions = db.query(User.UserID, User.UserName, User.UserImage)
    reactions = reactions.join(Reaction, User.UserID == Reaction.UserID)
    reactions = reactions.filter(Reaction.PublicationID == publication_id).all()
    
    comments = db.query(Comment.ContentComment, Comment.Date, User.UserID, User.UserName, User.UserImage)
    comments = comments.join(User, Comment.UserID == User.UserID)
    comments = comments.filter(Comment.PublicationID == publication_id).all()
    
    reaction_list = [
        UserBasicResponse(UserID=user_id, UserName=username, UserImage=user_image)
        for user_id, username, user_image in reactions if user_id is not None
    ]
    
    comment_list = [
        CommentResponseExtended(
            ContentComment=content,
            Date=date,
            User=UserBasicResponse(UserID=user_id, UserName=username, UserImage=user_image)
        )
        for content, date, user_id, username, user_image in comments if user_id is not None
    ]
    
    return DetailPublicationResponse(
        PublicationID=pub.PublicationID,
        ContentPubli=pub.ContentPubli,
        ImagePubli=pub.ImagePubli,
        Date=pub.Date,
        UserID=pub.UserID,
        CommentCount=comment_count,
        ReactionCount=reaction_count,
        Reactions=reaction_list,
        Comments=comment_list
    )

@router.get("/users/{user_id}/list_user_publications/", response_model=List[PublicationListResponseExtended])
def list_user_publications(user_id: int, db: Session = Depends(get_db)):
    publications = (db.query(
        Publication,
        func.count(Comment.CommentID).label("CommentCount"),
        func.count(Reaction.ReactionID).label("ReactionCount")
    ).outerjoin(Comment, Publication.PublicationID == Comment.PublicationID)
    .outerjoin(Reaction, Publication.PublicationID == Reaction.PublicationID)
    .filter(Publication.UserID == user_id)
    .group_by(Publication.PublicationID).all()
    )
    
    return [
        PublicationListResponseExtended(
            PublicationID=pub.PublicationID,
            ContentPubli=pub.ContentPubli,
            ImagePubli=pub.ImagePubli,
            Date=pub.Date,
            UserID=pub.UserID,
            CommentCount=comment_count,
            ReactionCount=reaction_count
        )
        for pub, comment_count, reaction_count in publications
    ]


@router.delete("/delete_publication/{publication_id}")
def delete_publication(publication_id: int, db: Session = Depends(get_db)):
    publication = db.query(Publication).filter(Publication.PublicationID == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    
    db.query(Comment).filter(Comment.PublicationID == publication_id).delete()
    db.query(Reaction).filter(Reaction.PublicationID == publication_id).delete()
    
    db.delete(publication)
    db.commit()
    return {"message": "Publicación eliminada exitosamente"}
