import pytest
from app import models

@pytest.fixture()
def test_vote(test_user,test_posts,session):
    new_vote=models.Vote(post_id =test_posts[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()



def test_vote_on_posts(authorize_client,test_posts,test_user):
    res=authorize_client.post("/vote/" , json={"post_id":test_posts[3].id, "dir":1 })
    assert res.status_code ==201

def test_vote_twice_post(authorize_client,test_posts,test_user,test_vote):
    res=authorize_client.post("/vote/", json={"post_id":test_posts[3].id, "dir":1 })
    assert res.status_code==409


#testing for deleting a post
def test_delete_vote(authorize_client, test_posts,test_vote,test_user):
    res = authorize_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201

#unlinking a post that was never liked
def test_delete_non_exist_vote(authorize_client, test_posts,test_user):
    res = authorize_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404

#test for liking a post that does not exists
def test_vote_post_non_exist(authorize_client,test_posts):
    res = authorize_client.post("/vote/", json={"post_id":8000, "dir": 1})
    assert res.status_code == 404

#unauthenticated user cant vote
def test_vote_unauth_vote(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401
