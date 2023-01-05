from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils, database, oauth2

router = APIRouter(
    tags=["Authentiaction"]
)

@router.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.Token)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Credentials does not match")
    # print(user)
    jwt_token = oauth2.create_access_token(data = {"user_id": user.id})
    return schemas.Token(access_token=jwt_token, token_type="bearer")
    