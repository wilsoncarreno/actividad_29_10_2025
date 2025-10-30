import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from inventario.app import app, db, Product
import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_create_product_success(client):
    data = {'nombre': 'Producto 1', 'precio': 10.5, 'stock': 100}
    response = client.post('/api/productos', json=data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['nombre'] == 'Producto 1'
    assert data['precio'] == 10.5
    assert data['stock'] == 100


def test_create_product_missing_fields(client):
    data = {'nombre': 'Producto 1'}
    response = client.post('/api/productos', json=data)
    assert response.status_code == 400


def test_get_products(client):
    # Create a product first
    data = {'nombre': 'Producto 1', 'precio': 10.5, 'stock': 100}
    client.post('/api/productos', json=data)

    response = client.get('/api/productos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['products']) == 1
    assert data['products'][0]['nombre'] == 'Producto 1'


def test_update_stock_success(client):
    # Create a product first
    data = {'nombre': 'Producto 1', 'precio': 10.5, 'stock': 100}
    response = client.post('/api/productos', json=data)
    product_id = json.loads(response.data)['id']

    update_data = {'stock': 150}
    response = client.put(f'/api/productos/{product_id}/stock', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['stock'] == 150


def test_update_stock_missing_field(client):
    # Create a product first
    data = {'nombre': 'Producto 1', 'precio': 10.5, 'stock': 100}
    response = client.post('/api/productos', json=data)
    product_id = json.loads(response.data)['id']

    update_data = {}
    response = client.put(f'/api/productos/{product_id}/stock', json=update_data)
    assert response.status_code == 400


def test_update_stock_not_found(client):
    update_data = {'stock': 150}
    response = client.put('/api/productos/999/stock', json=update_data)
    assert response.status_code == 404


def test_delete_product_success(client):
    # Create a product first
    data = {'nombre': 'Producto 1', 'precio': 10.5, 'stock': 100}
    response = client.post('/api/productos', json=data)
    product_id = json.loads(response.data)['id']

    response = client.delete(f'/api/productos/{product_id}')
    assert response.status_code == 200

    # Verify product is deleted
    response = client.get('/api/productos')
    data = json.loads(response.data)
    assert len(data['products']) == 0


def test_delete_product_not_found(client):
    response = client.delete('/api/productos/999')
    assert response.status_code == 404