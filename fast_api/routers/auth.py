from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from dependencies import get_db
from models.user import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'Safa2018'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

templates = Jinja2Templates(directory="templates")

class CreateUserRequest(BaseModel):
    email:str
    phone_number:str
    name:str
    surname:str
    password:str
    
class Token(BaseModel):
    access_token: str 
    token_type: str   
    

        
db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/',status_code=status.HTTP_201_CREATED)
async def user_sign_up(request: Request,\
                    db: db_dependency,
                    create_user_request: CreateUserRequest):
    create_user_model = User(
      email=create_user_request.email,
      phone_number=create_user_request.phone_number,
      name=create_user_request.name,
      surname=create_user_request.surname,
      hashed_password=bcrypt_context.hash(create_user_request.password) 
  ) 
  
    db.add(create_user_model)
    db.commit()
    


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = user_login(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.email, user.id, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}
    
    
    
def user_login(username: str, password: str, db):
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() +  expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)    


