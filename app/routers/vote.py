
from fastapi import Body,status,Response,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,oauth,schemas,database

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]

)

@router.post("/",status_code= status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {vote.post_id} does not exit")

    vote_query= db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    found_post = vote_query.first()

    if (vote.dir == 1):

        if found_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user  {current_user.id} have already voted for the post {vote.post_id}")

        new_vote=models.Vote(post_id = vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message":"vote successfully added"}
        
    else:
        if not found_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exit")

        vote_query.delete(synchronize_session=False)
        db.commit()  

        return{"message":"successfully delete vote"}      
      