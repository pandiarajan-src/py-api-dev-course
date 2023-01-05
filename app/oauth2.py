from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRECT = settings.secrect_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRY_TIME = settings.access_token_expiry_minutes

def create_access_token(data: dict):
    data_2_encode = data.copy()
    expiry_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_TIME)
    # data_2_encode['expiry'] = expiry_time
    data_2_encode.update({"expiry": str(expiry_time)})
    return jwt.encode(data_2_encode, SECRECT, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRECT, algorithms=[ALGORITHM])
        
        # If user id is  not valid, then raise an invalid credentials exception
        current_expiry_time = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRY_TIME)
        req_expiry_time = datetime.strptime(payload.get("expiry"), '%Y-%m-%d %H:%M:%S.%f')
        if current_expiry_time > req_expiry_time:
            raise credentials_exception
        
        # If user id is  not valid, then raise an invalid credentials exception
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        # Fill token data with valid user id
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    try:
        cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials!!!", headers={"WWW-Authenticate": "Bearer"})
        token_data = verify_access_token(token, cred_exception)
        # print(token_data)
        user = db.query(models.Users).filter(token_data.id == models.Users.id).first()
    except (JWTError, HTTPException) as ex:
        print(f"exception in get_current_user{ex.detail}")
        raise cred_exception

    return user

