from fastapi import FastAPI
from . import models
from .database import engine, SessionLocal
from .routers import post,user,auth,vote
from .config import settings

from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

pwd_context=CryptContext(schemes=["bcrypt"] , deprecated="auto")#all we are doing is we are telling the passlib what is the default hashing algorithm we wanna use aad in this case we are using bcrypt


#WILL NOT MODIFY TABLE ONLY CREATE A NEW TABLE IF ONE DOESNOT EXISTS
#models.Base.metadata.create_all(bind=engine)#this is to create tables for all the table models #no longer need this since we redid our models using alembic


#dependency,, session:stores  the objects in memory and keeps track of any changes needed in the data
# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()




app=FastAPI()

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

#the fastapi loads the code and looks for the first match  ORDER MATTERS

#class will represent what a post should look like 




# my_posts=[{"title":"title of post 1", "content":"content of title one","id":1},{"title":"fav foods","content":"i like pizza", "id": 2}]
#every time you save a piece of info within a database it is going to create a unique id identifier but here 
#since we donot have a databse rn so this will cause an error here becoz crud op needs an id so we'll add a field 

#not best practice there are other better ways
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
#
#
# def find_index_post(id):
#     for i, p  in enumerate(my_posts):
#         if p['id']==id:
#             return i






app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)









#path operation/route
#http methods:get post put head delete trace connect
@app.get('/')# root path '/' path we have to go in url #decorator-make this function an acutal path operation without this it is just a normal function 
async def root():#make thi sfunction as descriptive as possible 
    return {'message':"welcome to my api "}#it will automatically be converted to jason and sent back to the user



# # @app.get("/sqlalchemy")
# # def test_posts(db:Session= Depends(get_db)):

# #     posts = db.query(models.Post).all()
# #     return {"data" : posts}





# #getting post
# @app.get("/posts" ,response_model=List[schemas.Post])
# def get_posts(db:Session= Depends(get_db)):
#     #retiriving all our postss from our posts table

#     # posts=cursor.execute("""SELECT * FROM posts""")
#     # posts=cursor.fetchall()

#     posts = db.query(models.Post).all()
#     return posts #we can just pass in the python array and it will automaticaally be converted to json

# #creating post
# #whole idea is to send data    
 
# #how to retireve the body data for that we'll have to assign variables 
# #title str,content str


# # @app.post("/createposts")
# # def create_posts(payload:dict= Body(...)):#extract all the feilds from the body its going to convert them to  a python dict and store them inside a variable name payload
# #     print(payload)
# #     return{"new_post": f"title {payload['title']} content:{payload['content']}"}

# #in a real appliaction we will take the data and store it in our databases 

# #fastapi will validate it usign this post model defining what kind of data should frontend send
# @app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.Post) #correcting the default status code to 201 
# def create_posts(post:schemas.PostCreate, db:Session= Depends(get_db)):#the new_post here is storing it as  pydantic model
    
#     #cursor.execute(f"INSERT INTO posts (title , content , published ) VALUES ({post.title} , {post.content}  )")#this would work but would make you valnrable to sql injection
#     # cursor.execute(
#     #         """INSERT INTO posts (title,content,published) 
#     #            VALUES (%s, %s, %s) RETURNING *""",
#     #         (post.title, post.content, post.published)
#     #     ) #%s -varibles/place holders , this would make sure there is no extra sql command in there
#     # new_post=cursor.fetchone()
#     # conn.commit()#to save the data in the postgreee conmmit to them
    
#     # print(post)
#     # print(post.dict())
#     # post_dict=post.dict()
#     # pojst_dict['id']=randrange(0,1000000)
#     # my_posts.append(post_dict)

#    # new_post= models.Post(title= post.title,content= post.content , published=post.published)
#     new_post= models.Post(**post.dict())#instead of writting each coloumn seperately we can do tuple unpacking using this format ** is for tuple unpacking)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)


#     return new_post
# #when a front end send ddata to create new post after we create the new post and store it in put database we should return the newly created post with the id



# #retireving one individual post
# #id:-path parameter/ id of specific post
# @app.get("/posts/{id}", response_model=schemas.Post)
# def get_post(id : int , db:Session= Depends(get_db)):#response:Response
#     # cursor.execute(""" SELECT * from posts WHERE id= %s""" ,(str(id)))
#     # post=cursor.fetchone()

#     post= db.query(models.Post).filter(models.Post.id == id).first()
#     print(post)
#     if not post:
#         raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"post with id: {id} was not found" )     
#         # response.status_code = status.HTTP_404_NOT_FOUND       
#         # #instead of hard coding all this we can just use httpexception
#         # return {'message' : f"post with id: {id} was not found"}
#     return post
# #in case of path parameters alwasys tzke care of order cauz it could match it with any other get req which would cause error ###personal suggestion mini (keep them at bottom to avoid this)



# #error 404 :- http error/status code for this item does not exists 


# #create done , read done
# #deleting a post

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id : int, db:Session= Depends(get_db)):

#     # cursor.execute(""" DELETE FROM posts WHERE id= %s returning *""", (str(id),))
#     # deleted_post=cursor.fetchone()
#     # conn.commit()
#     #deleting post
#     #find the index in the array that has required id
#     #my_posts.pop(index)
#     # index=find_index_post(id)

#     post=db.query(models.Post).filter(models.Post.id == id)


#     if post.first()== None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exists")
#     # my_posts.pop(index)
#     post.delete(synchronize_session = False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
# #204 no content ensures that no content is sent



# #updating 
# @app.put("/posts/{id}", response_model=schemas.Post)
# def update_post(id : int ,updated_post:schemas.PostCreate, db:Session= Depends(get_db)): #making sure the request comes in , in the form of right schema we'll extend the post class
# #   cursor.execute(""" UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s RETURNING *""" , (post.title, post.content, post.published, str(id)))
# #   updated_post=cursor.fetchone()
# #   conn.commit()

#   post_query=db.query(models.Post).filter(models.Post.id == id)
#   post=post_query.first()

  
# #   index=find_index_post(id)

#   if post== None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exists")

        
#   post_query.update( updated_post.dict() , synchronize_session=False)
#   db.commit()




# #   post_dict=post.dict()
# #   post_dict['id'] = id
# #   my_posts[index]=post_dict
#   return post_query.first() 


# #fastapi has build in support for documentation automatically generates  docs/redocs


 

#################################################################################################################################################################################################################################################3
#users table
#we are going to create a new path operation for new user



# @app.post("/users" , status_code=status.HTTP_201_CREATED , response_model=schemas.UserOut)
# def create_user(user:schemas.Usercreate, db: Session = Depends(get_db)):
#     #has the password -user.password
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password

#     new_user= models.User(**user.dict())#instead of writting each coloumn seperately we can do tuple unpacking using this format ** is for tuple unpacking)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user 


# #route to retrieve user info based on their id /// think of it as when se search for other users on social media and their profile pops up
# @app.get('/users/{id}',response_model=schemas.UserOut)
# def get_user(id: int , db:Session = Depends(get_db)):
#     user=db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id :{id} does not exists")
    
#     return user
    
#router:-to split all our path operations to organise our code a lil bit better then inport them usoing app.inlcude_router(nameoffile.router)