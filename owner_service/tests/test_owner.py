def test_unique_buyers(owner_client):
    response = owner_client.get("/api/v1/owner/unique-buyers")
    assert response.status_code == 200
    data = response.json()
    assert "unique_buyers" in data
    assert isinstance(data["unique_buyers"], int)


def test_loyal_customers(owner_client):
    response = owner_client.get("/api/v1/owner/loyal-customers")
    assert response.status_code == 200
    data = response.json()
    assert "loyal_customers" in data
    assert isinstance(data["loyal_customers"], list)


def test_top_products(owner_client):
    response = owner_client.get("/api/v1/owner/top-products")
    assert response.status_code == 200
    data = response.json()
    assert "top_products" in data
    assert isinstance(data["top_products"], list)
    for product in data["top_products"]:
        assert "product_name" in product
        assert "times_was_purchased" in product


def test_get_top_products(owner_client):
    response = owner_client.get_top_products("/api/v1/owner/top-products")
    assert response.status_code == 200
    data = response.json()
    assert "top_products" in data
