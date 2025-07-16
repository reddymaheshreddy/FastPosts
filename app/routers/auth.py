from fastapi import  HTTPException, status, Response, Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..utils import verify
from .oauth2 import create_access_token
from typing import List
router=APIRouter(tags=["Authentication"])
@router.post("/login",response_model=schemas.Token)
def login(user:OAuth2PasswordRequestForm=Depends() , db: Session = Depends(get_db)):
    query=db.query(models.User).filter(models.User.email==user.username).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    password_matched = verify(user.password, query.password)
    if not password_matched:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token= create_access_token(data={"user_id": query.id})
    return {"access_token": access_token, "token_type": "bearer"}
    
