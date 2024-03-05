from tests.conftest import client


async def test_happy(client):
    data = {
        "email": "insert@example.com",
        "username": "insert",
        "password": "unused"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    body = response.json()
    assert body["email"] == "insert@example.com"
    assert body["username"] == "insert"


async def test_already_inside(client):
    data = {
        "email": "inside@example.com",
        "username": "inside",
        "password": "unused"
    }
    response = client.post("/auth/add_user", json=data)

    assert response.status_code == 200

    data = {
        "email": "inside@example.com",
        "username": "inside",
        "password": "unused"
    }
    response = client.post("/auth/add_user", json=data)

    assert response.status_code == 404


async def test_invalid_email(client):
    data = {
            "email": "invalidemailexample.com",
            "username": "invalidemail",
            "password": "unused"
    }
    response = client.post("/auth/add_user", json=data)

    assert response.status_code == 422


async def test_invalid_schema(client):
    data = {
        "email": "invalidschema@example.com",
        "username": "invalidschema"
    }
    response = client.post("/auth/add_user", json=data)

    assert response.status_code == 422
