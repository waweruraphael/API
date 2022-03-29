
from fastapi import Body, FastAPI,status,Response,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session

from app.oauth import get_current_user
from .. import models,utils,schemas,oauth
from .. database import get_db



router = APIRouter(
    prefix="/users",
    tags=["users"]
)


#create users

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)   
def create_user(users:schemas.UserCreate,db: Session = Depends(get_db)):


    #hashing password
    hashed = utils.hash(users.password)
    users.password = hashed

    new_user= models.User(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# get one user
@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):

    user=db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exit" )
        
    return user    
