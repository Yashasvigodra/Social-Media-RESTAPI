#all the path operations dealing with posts will be put in this file


# @app.get("/sqlalchemy")
# def test_posts(db:Session= Depends(get_db)):

#     posts = db.query(models.Post).all()
#     return {"data" : posts}


from .. import models, schemas,oauth2
from typing import List,Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func
from ..oauth2 import get_current_user

router=APIRouter(
    prefix="/posts", #/id      /posts/{id}
    tags=['posts']
                 )

#getting post
@router.get("/" ,response_model=List[schemas.PostOut])
def get_posts(db:Session= Depends(get_db),current_user:int=Depends(oauth2.get_current_user), limit: int=10,skip:int=0,search:Optional[str]=""):
    #retiriving all our postss from our posts table

    # posts=cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id ==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    response = [{"Post": post, "votes": votes} for post, votes in posts]
    return response
    #return posts #we can just pass in the python array and it will automaticaally be converted to json

#creating post
#whole idea is to send data    
 
#how to retireve the body data for that we'll have to assign variables 
#title str,content str


# @app.post("/createposts")
# def create_posts(payload:dict= Body(...)):#extract all the feilds from the body its going to convert them to  a python dict and store them inside a variable name payload
#     print(payload)
#     return{"new_post": f"title {payload['title']} content:{payload['content']}"}

#in a real appliaction we will take the data and store it in our databases 

#fastapi will validate it usign this post model defining what kind of data should frontend send
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post) #correcting the default status code to 201 
def create_posts(post:schemas.PostCreate, db:Session= Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):#the new_post here is storing it as  pydantic model
    



    #cursor.execute(f"INSERT INTO posts (title , content , published ) VALUES ({post.title} , {post.content}  )")#this would work but would make you valnrable to sql injection
    # cursor.execute(
    #         """INSERT INTO posts (title,content,published) 
    #            VALUES (%s, %s, %s) RETURNING *""",
    #         (post.title, post.content, post.published)
    #     ) #%s -varibles/place holders , this would make sure there is no extra sql command in there
    # new_post=cursor.fetchone()
    # conn.commit()#to save the data in the postgreee conmmit to them
    
    # print(post)
    # print(post.dict())
    # post_dict=post.dict()
    # pojst_dict['id']=randrange(0,1000000)
    # my_posts.append(post_dict)

   # new_post= models.Post(title= post.title,content= post.content , published=post.published)
    
    #print(current_user.email)
    new_post= models.Post(owner_id=current_user.id , **post.dict())#instead of writting each coloumn seperately we can do tuple unpacking using this format ** is for tuple unpacking)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post
#when a front end send ddata to create new post after we create the new post and store it in put database we should return the newly created post with the id



#retireving one individual post
#id:-path parameter/ id of specific post
@router.get(""
"/{id}", response_model=schemas.PostOut)
def get_post(id : int , db:Session= Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):#response:Response
    # cursor.execute(""" SELECT * from posts WHERE id= %s""" ,(str(id)))
    # post=cursor.fetchone()

    #post= db.query(models.Post).filter(models.Post.id == id).first()
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id ==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    #response = [{"Post": post, "votes": votes} for post, votes in posts]
    if not posts:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"post with id: {id} was not found" )     
        # response.status_code = status.HTTP_404_NOT_FOUND       
        # #instead of hard coding all this we can just use httpexception
        # return {'message' : f"post with id: {id} was not found"}
    post_data, vote_count = posts
    return {"Post": post_data, "votes": vote_count}
#in case of path parameters alwasys tzke care of order cauz it could match it with any other get req which would cause error ###personal suggestion mini (keep them at bottom to avoid this)



#error 404 :- http error/status code for this item does not exists 


#create done , read done
#deleting a post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db:Session= Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts WHERE id= %s returning *""", (str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    #deleting post
    #find the index in the array that has required id
    #my_posts.pop(index)
    # index=find_index_post(id)

    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()


    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")
    # my_posts.pop(index)

    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not authorised to perform requested action.")

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#204 no content ensures that no content is sent



#updating 
@router.put(""
"/{id}", response_model=schemas.Post)
def update_post(id : int ,updated_post:schemas.PostCreate, db:Session= Depends(get_db),current_user:int=Depends(oauth2.get_current_user)): #making sure the request comes in , in the form of right schema we'll extend the post class
#   cursor.execute(""" UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s RETURNING *""" , (post.title, post.content, post.published, str(id)))
#   updated_post=cursor.fetchone()
#   conn.commit()

  post_query=db.query(models.Post).filter(models.Post.id == id)
  post=post_query.first()

  
#   index=find_index_post(id)

  if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exists")


  if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action.")

        
  post_query.update( updated_post.dict() , synchronize_session=False)
  db.commit()




#   post_dict=post.dict()
#   post_dict['id'] = id
#   my_posts[index]=post_dict
  return post_query.first() 


#fastapi has build in support for documentation automatically generates  docs/redocs

