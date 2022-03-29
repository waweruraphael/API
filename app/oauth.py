from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas,database,models
from .config import settings



oauth_schemes = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM =  settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def access_token(data:dict):
    to_encode= data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    jwt_encode= jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_encode

def verify_access_token(token:str,credential_exception): 

    try:
        
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str = payload.get("user_id")

        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)  

    except JWTError:
        raise credential_exception

    return token_data    


def get_current_user(token:str= Depends(oauth_schemes),db:Session = Depends(database.get_db)): 
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"credential are not valid",headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token,credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()


    return user


        
    

