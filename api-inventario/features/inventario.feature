Feature: Gestión de Inventario de Productos

  Scenario: Crear un producto exitosamente
    Given que tengo datos válidos para un producto
    When envío una solicitud POST a /api/productos
    Then debería recibir una respuesta exitosa con el producto creado

  Scenario: Listar productos
    Given que existen productos en el inventario
    When envío una solicitud GET a /api/productos
    Then debería recibir una lista de productos con paginación

  Scenario: Actualizar stock de un producto
    Given que existe un producto con ID específico
    When envío una solicitud PUT a /api/productos/{id}/stock con nuevo stock
    Then el stock del producto debería actualizarse

  Scenario: Eliminar un producto existente
    Given que existe un producto con ID específico
    When envío una solicitud DELETE a /api/productos/{id}
    Then el producto debería eliminarse del inventario

  Scenario: Intentar eliminar un producto inexistente
    Given que no existe un producto con ID específico
    When envío una solicitud DELETE a /api/productos/{id}
    Then debería recibir un error 404