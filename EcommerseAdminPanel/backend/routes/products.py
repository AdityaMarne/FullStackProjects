from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection

products_bp = Blueprint('product', __name__, url_prefix='/api/products')

@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({"error":"Unauthorized"}),403
    
    data = request.json
    name = data['name']
    description = data.get('description', '')
    price = data['price']
    stock = data['stock']
    image_url = data.get('image_url', '')
    category_id = data['category_id']

    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO products (name, description, price, stock, image_url, category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, description, price, stock, image_url, category_id))
        db.commit()
        return jsonify({'message': 'Product created successfully'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error":str(e)}), 400
    
@products_bp.route('<int:id>', methods=['POST'])
def get_product(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("select * from products where id = %s", (id,))
    product = cursor.fetchone()
    if not product:
        return jsonify({'error':'Product not found'}), 404
    return jsonify(product)








