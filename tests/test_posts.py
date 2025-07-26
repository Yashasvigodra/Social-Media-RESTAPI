import pytest

from app import schemas


def test_get_all_posts(authorize_client,test_posts):
    res=authorize_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list= list(posts_map)

    # assert posts_list[0].Post.id==test_posts[0].id
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

#test that an unauthorize user cannot access posts
def test_unauthorized_user_get_all_posts(client, test_posts):
    res=client.get("/posts/")
    assert res.status_code == 401


#getting individual posts
def test_unauthorized_user_get_one_post(client, test_posts):
    res=client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code ==401

#test to retrive a post with an id that doesnt exists

def test_get_one_post_not_exist(authorize_client,test_posts):
    res=authorize_client.get("/post/8888")
    assert res.status_code == 404

#test for getting one individual post
def test_get_one_post(authorize_client, test_posts):
    res=authorize_client.get(f"/posts/{test_posts[0].id}")
    post=schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


#test for creating a post
@pytest.mark.parametrize("title, content , published" ,
                         [
                             ("aws new title" , "aws new content" , True),
                             ("fav pizza" , "papperoni" , False),
                             ("tallest" , "wahoo" , True)
                         ])
def test_create_post(authorize_client, test_posts, test_user , title , content, published):
    res=authorize_client.post("/posts/" , json={"title":title , "content": content, "published":published})
    created_post= schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
#     assert created_post.owner_id == test_user['id']
#
def test_create_post_default_published_true(authorize_client, test_posts,test_user):
    res=authorize_client.post("/posts/" , json={"title":"title" , "content": "content"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

#unauthorized user creating a post
def test_unauthorised_user_creaate_post(client, test_posts,test_user):
    res=client.post("/posts/" , json={"title":"title" , "content": "content"})
    assert res.status_code == 401


#tests for deleting in a post
#unauthorised user
def test_unauthorised_user_delete_post(client,test_posts,test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

#valid deletion
def test_delete_post_success(authorize_client, test_posts,test_user):
    res = authorize_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

#deleting a post with id that doesnt exists
def test_delete_post_non_exists(authorize_client,test_posts,test_user):
    res = authorize_client.delete(f"/posts/800000")
    assert res.status_code == 404

# def test_delete_other_user_post(authorize_client, test_posts, test_user):
#     # test_posts[3] belongs to test_user2
#     res = authorize_client.delete(f"/post/{test_posts[3].id}")
#     print(f"Post ID: {test_posts[3].id}, Owner: {test_posts[3].owner_id}")
#     print(f"Authorized user ID: {test_user['id']}")
#     # Optional debug
#     assert res.status_code == 403


#test for updating a post
def test_update_post(authorize_client,test_posts,test_user):
    data={
        "title": "new title",
        "content": "new content",
        "id":test_posts[0].id
    }
    res=authorize_client.put(f"/posts/{test_posts[0].id}" , json=data)
    updated_post=schemas.Post(**res.json())
    assert res.status_code==200
    assert updated_post.title==data['title']
    assert updated_post.content==data['content']

# def test_update_post_(authorize_client,test_posts,test_user,test_user2):
#     data={
#         "title": "new title",
#         "content": "new content",
#         "id":test_posts[3].id
#     }
#     res=authorize_client.put(f"/posts/{test_posts[3].id}" , json=data)
#     updated_post=schemas.Post(**res.json())
#     assert res.status_code==403



#unauthorize user trying to update a post
def test_unauthorised_user_update_post(client,test_posts,test_user):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

#updting a post that does not exists
def test_updating_post_non_exists(authorize_client,test_posts,test_user):
    data = {
        "title": "new title",
        "content": "new content",
        "id": test_posts[0].id
    }
    res = authorize_client.put(f"/posts/800000", json=data)
    assert res.status_code == 404






