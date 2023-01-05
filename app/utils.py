from passlib.context import CryptContext

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return hash_context.hash(password)

def verify_password(password: str, hashed_pwd: str):
    return hash_context.verify(secret=password, hash=hashed_pwd)
    