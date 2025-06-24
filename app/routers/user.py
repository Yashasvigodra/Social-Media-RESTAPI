#all path operations dealing with users will be put into this file

#to go up two dicrectory we use ..
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.UserOut)
def create_user(user:schemas.Usercreate, db: Session = Depends(get_db)):
    #has the password -user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user= models.User(**user.dict())#instead of writting each coloumn seperately we can do tuple unpacking using this format ** is for tuple unpacking)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 


#route to retrieve user info based on their id /// think of it as when se search for other users on social media and their profile pops up
@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id: int , db:Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id :{id} does not exists")
    
    return user
    