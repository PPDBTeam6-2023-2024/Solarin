
def insert_test_data(client):
    data = {
        "email": "insert@example.com",
        "username": "insert",
        "password": "mypass123!"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    data2 = {
        "email": "insert2@example.com",
        "username": "insert2",
        "password": "mypass123!"
    }
    response = client.post("/auth/add_user", json=data2)
    assert response.status_code == 200

    response = client.post("/auth/token", data=data, headers={
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    })

    assert response.status_code == 200

    body = response.json()
    token = body["access_token"]

    headers = {'Authorization': f"Bearer {token}",
               "content-type": "application/x-www-form-urlencoded",
               "accept": "application/json"
               }

    response2 = client.post("/auth/token", data=data2, headers={
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    })

    assert response2.status_code == 200

    body2 = response2.json()
    token2 = body2["access_token"]

    headers2 = {'Authorization': f"Bearer {token2}",
               "content-type": "application/x-www-form-urlencoded",
               "accept": "application/json"
               }

    return headers, headers2, token, token2


def test_friends(client):
    headers, headers2, token, token2 = insert_test_data(client)
    response = client.get("/chat/dm_overview", headers=headers2)

    """
    no friends, means an empty dm overview
    """
    assert response.json() == []

    """
    send friend request to 'insert' from 'insert2'
    """
    data = {
        "type": "add",
        "username": "insert"
    }
    response = client.post("/chat/friend_requests", json=data, headers=headers2)
    data = response.json()
    assert response.status_code == 200
    assert data["success"]
    assert data["message"] == 'Friend request has been send'

    """
    as insert accept friend request from 'insert2'
    """
    response = client.get("/chat/friend_requests", headers=headers)
    data = response.json()
    assert len(data) == 1
    assert data[0][0] == "insert2"
    assert data[0][1] == 2 # user id

    """
    'insert' will accept the friend request from 'insert2'
    """
    data = {
        "type": "review",
        "friend_id": 2,
        "accepted": True
    }
    response = client.post("/chat/friend_requests", headers=headers, json=data)
    data = response.json()
    assert data["success"]
    assert data["message"] == 'Friend request has been accepted'

    """
    recheck the dm overview of 'insert2'
    """

    response = client.get("/chat/dm_overview", headers=headers2)
    data = response.json()
    assert len(data) == 1
    assert data[0][0] == "insert"
    assert data[0][1]["body"] == "Friend request has been accepted"


def test_alliance(client):
    headers, headers2, token, token2 = insert_test_data(client)

    """
    let 'insert' create an alliance
    """
    data = {
        "alliance_name": "abc"
    }
    response = client.post("/chat/create_alliance", headers=headers, json=data)
    data = response.json()
    assert data["success"]
    assert data["message"] == "Alliance is created"

    """
    let 'insert2' send an alliance join request to alliance 'abc'
    """

    data = {
        "alliance_name": "abc"
    }
    response = client.post("/chat/join_alliance", headers=headers2, json=data)
    data = response.json()

    assert not data["success"]
    assert data["message"] == "Alliance join request has been send"

    """
    check for join alliance requests
    """
    response = client.get("/chat/alliance_requests", headers=headers)
    data = response.json()
    assert len(data) == 1
    assert data[0][0] == "insert2"

def test_alliance_kick(client):
    headers, headers2, token, token2 = insert_test_data(client)

    """
    let 'insert' create an alliance
    """
    data = {
        "alliance_name": "abc"
    }
    response = client.post("/chat/create_alliance", headers=headers, json=data)
    data = response.json()
    assert data["success"]
    assert data["message"] == "Alliance is created"

    """
    kick yourself from the alliance
    """

    response = client.post("/chat/kick_user", headers=headers, json={"user_id": 1})

    data = {
        "alliance_name": "abc"
    }
    response = client.post("/chat/alliance_messageboard", headers=headers2, json=data)
    data = response.json()
    assert data["detail"] == "Method Not Allowed"
