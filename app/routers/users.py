
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

###########
# Users API
###########
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # print(user.dict())
    user.password = utils.hash_password(user.password)
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    if new_user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"post with id:{id} is not found")    
    return new_user    


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} not found")
    return user
