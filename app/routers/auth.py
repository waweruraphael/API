
from tokenize import Token
from fastapi import HTTPException,responses,APIRouter,Depends,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from ..  import database,models,utils,oauth

router = APIRouter(tags=['Authentication'])


@router.post("/login",response_model= schemas.Token)
def login(user_credential:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):
    user= db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")

    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials ")

    token = oauth.access_token(data={"user_id":user.id})  

    return{"access_token":token,"token_type":"Bearer"} 
