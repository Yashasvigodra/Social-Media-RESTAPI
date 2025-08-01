from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db,Base
from alembic import command
import pytest
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine=create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal=sessionmaker(autocommit=False , autoflush=False, bind=engine )



Base.metadata.create_all(bind=engine)





@pytest.fixture()
def session():
    # command.upgrade("head")
    # command.downgrade("base")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


#setting testclient to a variable
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


#function that will return a user
@pytest.fixture()
def test_user2(client):
    user_data={"email":"yashasviii@gmail.com" ,"password": "mini"}
    res=client.post("/users/" ,json=user_data)
    assert res.status_code==201
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user
@pytest.fixture()
def test_user(client):
    user_data={"email":"yashasvi@gmail.com" ,"password": "mini"}
    res=client.post("/users/" ,json=user_data)
    assert res.status_code==201
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture()
def authorize_client(token, client):
    client.headers.update({
        "Authorization": f"Bearer {token}"  # Notice the space!
    })
    return client

@pytest.fixture()
def test_posts(test_user,test_user2 ,session):
    posts_data=[
        {"title" : "first title",
         "content"  : "first content" ,
         "owner_id" : test_user['id']},
        {
            "title": "second title",
            "content" :  "second content",
            "owner_id" : test_user['id']
        },
        {
            "title": "third title",
            "content":"third column",
            "owner_id" : test_user['id']
        },
        {
            "title": "diff user",
            "content": "diff content",
            "owner_id": test_user2['id']
        }
    ]
    def create_post_model(post):
        return models.Post(**post)
    post_map=map(create_post_model , posts_data)
    posts=list(post_map)
    session.add_all(posts)
    session.commit()
    posts=session.query(models.Post).all()
    return posts


