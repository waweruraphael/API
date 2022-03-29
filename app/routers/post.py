from fastapi import Body, FastAPI,status,Response,HTTPException,Depends,APIRouter
from typing import List,Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models,schemas,oauth
from .. database import get_db

router = APIRouter(

    prefix="/posts",
    tags=['Posts']
)


#fetch posts

@router.get("/",response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user:int =Depends(oauth.get_current_user),
limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts=cursor.fetchall()
    #posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id ==models.Post.id,
     isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    return posts


# @router.get("/test")
# def test_code(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     return{"status":post}

 # creating posts
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db: Session = Depends(get_db), current_user:int =Depends(oauth.get_current_user) ):
    # cursor.execute(""" INSERT INTO posts (title,content,publish) VALUES (%s,%s,%s) RETURNING * """,
    # (post.title,post.content,post.publish))
    
    # posted = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    posted = models.Post(user_id =current_user.id ,**post.dict())
    db.add(posted)
    db.commit()
    db.refresh(posted)
    
    return posted
    
# start fetch post per Id
@router.get("/{id}",response_model=schemas.PostVote)
def get_post(id:int,db: Session = Depends(get_db), current_user:int =Depends(oauth.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post =cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id ==models.Post.id,
     isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
        detail={'message':f"post with id {id} not found "})
            
    print(post)
    return post


# start delete posts
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user:int =Depends(oauth.get_current_user)):
    # cursor.execute(""" delete from posts where id =%s returning *""",(str(id),))
    # index = cursor.fetchone()
    # conn.commit()

    #index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_delete= post_query.first()

    if post_delete == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} does not exit ")

    if post_delete.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorised to perform the requested action")    

    post_query.delete(synchronize_session=False)
    db.commit()    
      
    return Response(status_code=status.HTTP_204_NO_CONTENT )


# updating posts    
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int,post:schemas.PostCreate,db: Session = Depends(get_db), current_user:int =Depends(oauth.get_current_user)):
    # cursor.execute("""UPDATE posts set title = %s,content=%s,publish=%s where id =%s returning * """
    # ,(post.title,post.content,post.publish,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    update_query = db.query(models.Post).filter(models.Post.id == id) 
    update_post = update_query.first()


    if update_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} does not exit ")

    if update_post.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorised to perform the requested action")      

    update_query.update(post.dict(),synchronize_session=False) 
    db.commit()  

    return update_query.first()