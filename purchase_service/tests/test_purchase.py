# from fastapi.testclient import TestClient
# from purchase_service.main import app
#
# client = TestClient(app)
#
# def test_get_products():
#     response = client.get("/api/v1/customer/products")
#     assert response.status_code == 200
#     data = response.json()
#     assert "Products" in data
#     assert isinstance(data["Products"], list)
#
#
# def test_make_purchase_new_user():
#     payload = {
#         "existing": "no",
#         "supermarket_id": "SMKT001",
#         "items": ["milk", "bread"]
#     }
#     response = client.post("/api/v1/customer/purchase", data=payload)
#     assert response.status_code == 200
#     result = response.json()
#     assert result["supermarket_id"] == payload["supermarket_id"]
#     assert result["total_amount"] > 0
#
#
# def test_make_purchase_existing_user():
#     # Make initial purchase to create user
#     payload = {
#         "existing": "no",
#         "supermarket_id": "SMKT001",
#         "items": ["eggs"]
#     }
#     response = client.post("/api/v1/customer/purchase", data=payload)
#     assert response.status_code == 200
#     user_id = response.json()["user_id"]
#
#     # Make another purchase with existing user
#     payload_existing = {
#         "existing": "yes",
#         "user_id": user_id,
#         "supermarket_id": "SMKT001",
#         "items": ["eggs"]
#     }
#     response_existing = client.post("/api/v1/customer/purchase", data=payload_existing)
#     assert response_existing.status_code == 200
#     assert response_existing.json()["user_id"] == user_id
#
#
# # def test_get_products(purchase_client):
# #     response = purchase_client.get("/api/v1/customer/products")
# #     assert response.status_code == 200
# #     data = response.json()
# #     assert "Products" in data
# #     assert len(data["Products"]) > 0

def test_get_products(purchase_client):
    response = purchase_client.get("/api/v1/customer/products")
    assert response.status_code == 200
    data = response.json()
    assert "Products" in data
    assert isinstance(data["Products"], list)

def test_make_purchase_new_user(purchase_client):
    payload = {
        "existing": "no",
        "supermarket_id": "SMKT001",
        "items": ["milk", "bread"]
    }
    response = purchase_client.post("/api/v1/customer/purchase", data=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["supermarket_id"] == payload["supermarket_id"]
    assert result["total_amount"] > 0