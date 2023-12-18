from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status,HTTPException,Response
from typing import List
from .. import utils,oauth2
 
 
router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/",response_model=List[schemas.PostResponse])
async def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    
    

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db),get_current_user:id = Depends(oauth2.get_current_user)):
    new_post = models.Post(title=post.title,content=post.content,published=post.published,rating=post.rating)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
  



@router.get("/{post_id}",response_model=schemas.PostResponse)
async def get_post(post_id:str , db:Session = Depends(get_db), ):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post
    
  

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:str,db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.patch("/{post_id}")
async def update_post(post_id:str,updated_post:schemas.PostCreate,db:Session = Depends(get_db)):
    print("hello world")
    post_query  = db.query(models.Post).filter(models.Post.id == post_id)
    
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    
    return post_query.first()
 