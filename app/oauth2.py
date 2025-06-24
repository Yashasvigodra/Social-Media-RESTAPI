from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas, database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from .config import settings


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
#secret_key
#algorith
#expiration time:-how long a user can log in after they enter the credentials

SECRET_KEY=settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minute

def create_access_token(data: dict):
    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" :expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


#verfuy access token

def verify_access_token(token: str, credentials_exception):
   
   try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        id: str=payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=str(id))
   except JWTError:
        raise credentials_exception
   
   return token_data
   
#paass thid function as a dependency into any of our path operation and whats its goining to do is take the token from the request automatically extract the ID for us ,its going to verify that the token is correct useing the verify_access_token, then its going to extract the id and if wwe want to we cant make it automatically fetch the user from the database and then add it into as a parameter into our path operataiton function 

def get_current_user(token : str=Depends(oauth2_scheme),db: session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    
    token=verify_access_token(token,credentials_exception)
    
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user
   

#we need to make sure the user is logedin before they can peform certain tasks