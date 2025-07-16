from .. import models, schemas
from fastapi import  HTTPException, status, Response, Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List,Optional
from .oauth2 import get_current_user    

router = APIRouter(prefix="/posts",tags=["Posts"])   

# Get all posts
@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db),limit: int = 5,skip:int=0,search: Optional[str] = ""):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id) .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results
# Get single post
@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post =db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post

# Create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),user_id: int = Depends(get_current_user)):
   
    new_post = models.Post(owner_id=user_id.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),user_id: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post= post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(post_query,synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    post_query.update(updated_post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return post_query.first()