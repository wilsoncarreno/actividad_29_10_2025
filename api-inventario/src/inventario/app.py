from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_args
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock
        }

@app.route('/api/productos', methods=['POST'])
def create_product():
    data = request.get_json()
    if not all(key in data for key in ('nombre', 'precio', 'stock')):
        return jsonify({'error': 'Missing required fields'}), 400

    product = Product(
        nombre=data['nombre'],
        precio=data['precio'],
        stock=data['stock']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@app.route('/api/productos', methods=['GET'])
def get_products():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    products_query = Product.query
    products = products_query.offset(offset).limit(per_page).all()
    total = products_query.count()

    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return jsonify({
        'products': [product.to_dict() for product in products],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': len(pagination.pages) if hasattr(pagination.pages, '__len__') else 1
        }
    })

@app.route('/api/productos/<int:id>/stock', methods=['PUT'])
def update_stock(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    if 'stock' not in data:
        return jsonify({'error': 'Stock field required'}), 400

    product.stock = data['stock']
    db.session.commit()
    return jsonify(product.to_dict())

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)