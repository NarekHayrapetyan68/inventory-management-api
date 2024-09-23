import pytest
from fastapi.testclient import TestClient
from app.main import api
from app.database import Base, engine
from app import crud, schemas


client = TestClient(api)


@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    client = TestClient(api)
    yield client
    Base.metadata.drop_all(bind=engine)

def test_create_product():
    response = client.post("/products/", json={"name": "Item", "description": "Description", "price": 100.0, "stock": 50})
    assert response.status_code == 200
    assert response.json()["name"] == "Item"


sample_product = {
    "name": "Test Product",
    "description": "Test Description",
    "price": 10.0,
    "quantity": 100,
}

def test_read_products(test_client):
    response = test_client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_product(test_client):
    response = test_client.get("/products/1")
    assert response.status_code == 200

def test_update_product(test_client):
    updated_product = {**sample_product, "price": 15.0}
    response = test_client.put("/products/1", json=updated_product)
    assert response.status_code == 200
    assert response.json()["price"] == updated_product["price"]

def test_delete_product(test_client):
    response = test_client.delete("/products/1")
    assert response.status_code == 200
    assert response.json()["message"] == "item was deleted"


def test_create_order(test_client):
    sample_order = {
        "product_id": 1,
        "quantity": 2,
    }
    response = test_client.post("/orders/", json=sample_order)
    assert response.status_code == 200

def test_read_orders(test_client):
    response = test_client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_order_status(test_client):
    response = test_client.patch("/orders/1/status", json={"status": "shipped"})
    assert response.status_code == 200

