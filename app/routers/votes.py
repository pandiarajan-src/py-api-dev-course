
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_posts(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post: {vote.post_id} does not exists")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.post_dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user: {current_user.id} has already voted to the post: {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : f"user: {current_user.id} has successfully voted for the post:{vote.post_id}"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user: {current_user.id} does not exist for the post: {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : f"successfully deleted vote for user: {current_user.id} post:{vote.post_id}"}




