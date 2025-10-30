# API Inventario

Una API REST completa para la gestión de inventario de productos, construida con Flask y SQLAlchemy. Incluye pruebas unitarias, pruebas BDD con Behave y pruebas de carga con Locust.

## Características

- ✅ API REST completa con 4 endpoints CRUD
- ✅ Persistencia de datos con SQLite y SQLAlchemy
- ✅ Paginación de resultados
- ✅ Validación de datos y manejo de errores
- ✅ Suite completa de pruebas unitarias (94% cobertura)
- ✅ Pruebas BDD con Behave (5 escenarios)
- ✅ Pruebas de carga con Locust
- ✅ Gestión de dependencias con Poetry

## Tecnologías Utilizadas

- **Flask**: Framework web para la API
- **SQLAlchemy**: ORM para la base de datos
- **Flask-Paginate**: Paginación de resultados
- **Poetry**: Gestión de dependencias y empaquetado
- **pytest**: Framework de pruebas unitarias
- **pytest-mock**: Mocking para pruebas
- **coverage**: Análisis de cobertura de código
- **Behave**: Pruebas BDD con Gherkin
- **Locust**: Pruebas de carga y rendimiento

## Instalación

1. **Requisitos previos**:
   - Python 3.11+
   - Poetry instalado

2. **Instalación**:
   ```bash
   cd api-inventario
   poetry install
   ```

## Uso

### Ejecutar la API

```bash
poetry run python src/inventario/app.py
```

La API estará disponible en `http://localhost:5000`

### Endpoints de la API

#### Crear Producto
```http
POST /api/productos
Content-Type: application/json

{
  "nombre": "Producto Ejemplo",
  "precio": 25.99,
  "stock": 100
}
```

#### Listar Productos
```http
GET /api/productos?page=1&per_page=10
```

#### Actualizar Stock
```http
PUT /api/productos/{id}/stock
Content-Type: application/json

{
  "stock": 150
}
```

#### Eliminar Producto
```http
DELETE /api/productos/{id}
```

## Pruebas

### Pruebas Unitarias

Ejecutar todas las pruebas unitarias:
```bash
poetry run pytest
```

Con reporte de cobertura:
```bash
poetry run coverage run -m pytest
poetry run coverage report --include=src/*
```

### Pruebas BDD

Ejecutar pruebas con Behave:
```bash
poetry run behave
```

### Pruebas de Carga

Ejecutar Locust (interfaz web):
```bash
poetry run locust -f locustfile.py --host=http://localhost:5000
```

Acceder a la interfaz web en `http://localhost:8089`

Configurar prueba:
- Número de usuarios: 50
- Tasa de spawn: 2 usuarios/segundo
- Duración: 5 minutos

## Estructura del Proyecto

```
api-inventario/
├── src/inventario/
│   ├── __init__.py
│   └── app.py              # Aplicación Flask principal
├── tests/
│   └── test_app.py         # Pruebas unitarias
├── features/
│   ├── inventario.feature  # Escenarios BDD
│   └── steps/
│       └── inventario_steps.py  # Implementación de steps
├── locustfile.py           # Configuración de pruebas de carga
├── pyproject.toml          # Configuración de Poetry
├── poetry.lock             # Lock file de dependencias
└── README.md               # Este archivo
```

## Modelo de Datos

### Producto
- `id`: Identificador único (autoincremental)
- `nombre`: Nombre del producto (string, requerido)
- `precio`: Precio del producto (float, requerido)
- `stock`: Cantidad en inventario (integer, requerido)

## Cobertura de Pruebas

- **Líneas**: 94%
- **Funciones**: 100%
- **Ramas**: 83%

## Configuración de Pruebas de Carga

El archivo `locustfile.py` incluye:

- **Pesos de tareas**:
  - Crear producto: 3
  - Listar productos: 4
  - Actualizar stock: 2
  - Eliminar producto: 1

- **Tiempo de espera**: Entre 1-3 segundos entre requests
- **Autenticación inicial**: Crea un producto de prueba al iniciar

## Desarrollo

### Agregar nuevas dependencias

```bash
poetry add nombre-paquete
```

### Actualizar dependencias

```bash
poetry update
```

### Ejecutar en modo desarrollo

```bash
poetry run flask --app src/inventario/app.py run --debug
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.