from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get('/', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # To return posts of all users
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    # to return posts of only the specific owner of the post
    # posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
    if len(posts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts were found")
    return posts

@router.get('/latest', response_model=schemas.Post)
async def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).order_by(models.Posts.created_at.desc()).limit(1).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts were found")
    return post

@router.get('/{id}', response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), 
                    current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} is not found")
    return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(payload: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(payload.dict())
    print(f"userid from token validation is: {current_user.id}")
    my_post = payload.dict()
    # new_post = models.Posts(title=payload.title, content=payload.content, published=payload.published, rating=payload.rating)
    new_post = models.Posts(owner_id=current_user.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    if new_post is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"post with id:{id} is not found")    
    return new_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, )
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    elif post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"post {id} doesn't belong to user: {current_user.id}")     
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_posts(id: int, payload: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")        
    elif post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"post {id} doesn't belong to user: {current_user.id}")          
    else:
        post.update(payload.dict(), synchronize_session=False)
        db.commit()
        return post.first()

