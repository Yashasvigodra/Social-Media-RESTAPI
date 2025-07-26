from app import schemas

import pytest
from jose import jwt
from app.config import settings




#testing root
# def test_root(client, session):
#     res=client.get("/")
#     assert res.json().get('message').strip() == 'welcome to my api'
#     assert res.status_code ==200

#dont make test depend on other test each test should exist independently
def test_create_user(client, session):
    res=client.post("/users/" , json={"email" : "hello123@gmail.com", "password" : "password123"})
    print(res.json())
    new_user= schemas.UserOut(**res.json())

    assert res.status_code ==201
    assert new_user.email == "hello123@gmail.com"

def test_login_user(client,test_user):
    res=client.post("/login", data={"username" : test_user['email'], "password" : test_user['password']})
    login_res=schemas.Token(**res.json())
    payload=jwt.decode(login_res.access_token, settings.secret_key,algorithms=[settings.algorithm])
    id=payload.get("user_id")
    assert id==test_user['id']
    assert login_res.token_type == "bearer"

    assert res.status_code==200


#test for failed login
@pytest.mark.parametrize("email,password,status_code",
                         [
                             ('wrongemail@gmail.com', "mini", 403),
                             ('yashasvi@gmail.com', 'wrongp', 403),
                             ('wrong@gmail.com', 'wrongp', 403),
                             (None, "mini", 422),
                             ("yashasvi@gmail.com", None, 422)
                         ])
def test_failed_login(client, test_user, email, password, status_code):
    data = {}
    if email is not None:
        data["username"] = email
    if password is not None:
        data["password"] = password

    res = client.post("/login", data=data)
    assert res.status_code == status_code

    # assert res.json().get('detail') == 'invalid credentials'
