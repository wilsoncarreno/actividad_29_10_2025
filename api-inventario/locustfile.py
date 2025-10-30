from locust import HttpUser, task, between
import json


class InventoryUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Crear un producto inicial para las pruebas
        self.product_data = {
            "nombre": "Producto de Prueba",
            "precio": 25.99,
            "stock": 100
        }
        response = self.client.post("/api/productos", json=self.product_data)
        response.raise_for_status()
        self.product_id = response.json()['id']

    @task(3)
    def create_product(self):
        data = {
            "nombre": f"Producto {self.user_id}",
            "precio": 10.50,
            "stock": 50
        }
        response = self.client.post("/api/productos", json=data)
        response.raise_for_status()

    @task(4)
    def get_products(self):
        response = self.client.get("/api/productos")
        response.raise_for_status()

    @task(2)
    def update_stock(self):
        data = {"stock": 75}
        response = self.client.put(f"/api/productos/{self.product_id}/stock", json=data)
        response.raise_for_status()

    @task(1)
    def delete_product(self):
        # Crear un producto temporal para eliminar
        data = {"nombre": "Producto Temporal", "precio": 5.0, "stock": 10}
        response = self.client.post("/api/productos", json=data)
        if response.status_code == 201:
            temp_product_id = response.json()['id']
            response = self.client.delete(f"/api/productos/{temp_product_id}")
            response.raise_for_status()