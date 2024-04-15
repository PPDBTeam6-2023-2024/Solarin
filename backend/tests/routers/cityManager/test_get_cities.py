
async def test_get_cities(client):
    response = client.get("/cityManager/cities", params={"planet_id": 1})
    assert response.status_code == 200
