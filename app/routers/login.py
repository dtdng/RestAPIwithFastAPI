from fastapi import APIRouter, Depends, status, HTTPException
from hash import Hash
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import models, database, JWTToken
from datetime import timedelta

router = APIRouter(
    prefix='/login',
    tags=["Login"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not Hash.verify_password(request.password, user.password_hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTToken.create_access_token(
        data={"sub": user.username, "scopes": request.scopes}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}