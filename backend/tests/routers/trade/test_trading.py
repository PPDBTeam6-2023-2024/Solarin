from src.app.database.database_access.data_access import DataAccess
from src.app.database.database import sessionmanager


async def test_see_trade(client, data_access: DataAccess):
    data = {
        "email": "insert@example.com",
        "username": "test",
        "password": "test"
    }
    response = client.post("/auth/add_user", json=data)
    assert response.status_code == 200

    user_id = await data_access.UserAccess.get_user_id_email(
        email="insert@example.com"
    )

    await data_access.AllianceAccess.create_alliance("AAP")
    await data_access.AllianceAccess.set_alliance(user_id, "AAP")

    """
    Create second user
    """
    user_2 = await data_access.UserAccess.create_user("a", "a", "a")

    await data_access.ResourceAccess.add_resource(user_id, "SOL", 20)
    await data_access.ResourceAccess.add_resource(user_2, "TF", 3)

    await data_access.AllianceAccess.set_alliance(user_2, "AAP")

    await data_access.commit()

    await data_access.TradeAccess.create_trade_offer(user_2, [("SOL", 1)], [("TF", 2)])

    await data_access.commit()

    data = {
        "username": "test",
        "password": "test"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json",
    }
    response = client.post("/auth/token", data=data, headers=headers)
    assert response.status_code == 200

    body = response.json()
    assert body["token_type"] == "bearer"
    token = body["access_token"]

    with client.websocket_connect(f"/trading/ws", subprotocols=[token]) as websocket:
        websocket.send_json({
            "type": "get_trades"

        })

        data = websocket.receive_json()
        assert data["action"] == "show_trades"
        trades = data["trades"]
        assert len(trades) == 1
        assert trades[0]["user_id"] == 2
        assert trades[0]["offer_id"] == 1
        assert trades[0]["gives"] == [["SOL", 1]]
        assert trades[0]["receives"] == [["TF", 2]]

    return token


async def test_accept_trade(client, data_access: DataAccess):
    token = await test_see_trade(client, data_access)

    with client.websocket_connect(f"/trading/ws", subprotocols=[token]) as websocket:
        websocket.send_json({
            "type": "accept_trade",
            "offer_id": 1
        })

        data = websocket.receive_json()

        assert data["action"] == "show_trades"
        trades = data["trades"]
        assert len(trades) == 0


async def test_cancel_trade(client, data_access: DataAccess):
    token = await test_see_trade(client, data_access)

    with client.websocket_connect(f"/trading/ws", subprotocols=[token]) as websocket:
        websocket.send_json({
            "type": "create_trade",
            "gives": [("TF", 3)],
            "receives": [("SOL", 6)]
        })

        data = websocket.receive_json()
        assert data["action"] == "show_trades"
        trades = data["trades"]
        own_trades = data["own_offers"]
        assert len(trades) == 1
        assert len(own_trades) == 1
        assert own_trades[0]["user_id"] == 1

        websocket.send_json({
            "type": "cancel_trade",
            "offer_id": 2
        })

        data = websocket.receive_json()
        own_trades = data["own_offers"]
        assert len(own_trades) == 0


