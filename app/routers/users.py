from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
import models, schemas, database, oauth2
from hash import Hash
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel, ValidationError


router = APIRouter(
    prefix="/user",
    tags=['Users'],
    dependencies=None,
    responses=None
)
get_db = database.get_db

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={"me": "do something", "student": "read information"}
    )

@router.post('/')
def create_user(request: schemas.UserInput, db: Session = Depends(get_db), verify: schemas.User = Depends(oauth2.verify_user)):
    new_user = models.User(
        name=request.name, 
        username=request.username,
        password_hashed=Hash.get_password_hash(request.password)
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', response_model=List[schemas.User])
def all(db: Session = Depends(get_db), verify: schemas.User = Depends(oauth2.verify_user)):
    user_data = db.query(models.User).all()
    if user_data is None:
        raise HTTPException(status_code=404, detail="DB is empty")
    return user_data


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

@router.get("/me/")
async def read_users_me(current_user: schemas.User = Security(get_current_user, scopes=["me"])):
    return current_user
