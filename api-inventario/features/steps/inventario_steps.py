import requests
from behave import given, when, then
import json

BASE_URL = "http://localhost:5000"

@given('que tengo datos válidos para un producto')
def step_impl(context):
    context.product_data = {
        "nombre": "Producto de Prueba",
        "precio": 25.99,
        "stock": 50
    }

@given('que existen productos en el inventario')
def step_impl(context):
    # Crear algunos productos para las pruebas
    products = [
        {"nombre": "Producto 1", "precio": 10.0, "stock": 100},
        {"nombre": "Producto 2", "precio": 20.0, "stock": 200}
    ]
    context.created_products = []
    for product in products:
        response = requests.post(f"{BASE_URL}/api/productos", json=product)
        if response.status_code == 201:
            context.created_products.append(response.json())

@given('que existe un producto con ID específico')
def step_impl(context):
    # Crear un producto para las pruebas
    product_data = {"nombre": "Producto para Actualizar", "precio": 15.0, "stock": 75}
    response = requests.post(f"{BASE_URL}/api/productos", json=product_data)
    assert response.status_code == 201
    context.product = response.json()
    context.product_id = context.product['id']

@given('que no existe un producto con ID específico')
def step_impl(context):
    context.product_id = 99999  # ID que no existe

@when('envío una solicitud POST a /api/productos')
def step_impl(context):
    context.response = requests.post(f"{BASE_URL}/api/productos", json=context.product_data)

@when('envío una solicitud GET a /api/productos')
def step_impl(context):
    context.response = requests.get(f"{BASE_URL}/api/productos")

@when('envío una solicitud PUT a /api/productos/{{id}}/stock con nuevo stock')
def step_impl(context):
    update_data = {"stock": 150}
    context.response = requests.put(f"{BASE_URL}/api/productos/{context.product_id}/stock", json=update_data)

@when('envío una solicitud DELETE a /api/productos/{{id}}')
def step_impl(context):
    context.response = requests.delete(f"{BASE_URL}/api/productos/{context.product_id}")

@then('debería recibir una respuesta exitosa con el producto creado')
def step_impl(context):
    assert context.response.status_code == 201
    data = context.response.json()
    assert 'id' in data
    assert data['nombre'] == context.product_data['nombre']
    assert data['precio'] == context.product_data['precio']
    assert data['stock'] == context.product_data['stock']

@then('debería recibir una lista de productos con paginación')
def step_impl(context):
    assert context.response.status_code == 200
    data = context.response.json()
    assert 'products' in data
    assert 'pagination' in data
    assert isinstance(data['products'], list)

@then('el stock del producto debería actualizarse')
def step_impl(context):
    assert context.response.status_code == 200
    data = context.response.json()
    assert data['stock'] == 150

@then('el producto debería eliminarse del inventario')
def step_impl(context):
    assert context.response.status_code == 200
    # Verificar que el producto ya no existe
    response = requests.get(f"{BASE_URL}/api/productos")
    data = response.json()
    product_ids = [p['id'] for p in data['products']]
    assert context.product_id not in product_ids

@then('debería recibir un error 404')
def step_impl(context):
    assert context.response.status_code == 404