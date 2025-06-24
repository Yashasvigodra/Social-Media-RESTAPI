from fastapi import APIRouter, Depends, status, HTTPException,Response
from sqlalchemy.orm import session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schemas,models,utils,oauth2


router=APIRouter(
    tags=['Authentication']
)

@router.post('/login',response_model=schemas.Token)
         #  user_credentials: schemas.UserLogin
def login(user_credentials: OAuth2PasswordRequestForm=Depends(),db:session =Depends(database.get_db)):
   # {
   #     "username":"lksdl",
   #     "password":" dlmwle"
   # }
   
   user=db.query(models.User).filter(models.User.email==user_credentials.username).first()

   if not user:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
   if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")
   #create token
   #return token
   access_token=oauth2.create_access_token(data={"user_id":user.id})

   return {"access_token":access_token,"token_type":"bearer"}#just search jwt on web and there you can paste you jwt token and can decode it similarly anybody can do that

#verify the token is still valid and there hasn't been any tempering done with it 
