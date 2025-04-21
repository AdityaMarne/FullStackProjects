from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection

categories_bp  = Blueprint('categories', __name__, url_prefix='/api/categories')

@categories_bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({"error":"Unauthorized"}), 403
    
    data = request.json()
    name = data['name']
    description = data.get('description', '')

    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (name, description))
        db.commit()
        return jsonify({'message': 'Category created'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    
@categories_bp.route("/", methods=['GET'])
def get_all_categories():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    return jsonify(categories)

@categories_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE categories SET name = %s, description = %s WHERE id = %s",
                       (data['name'], data['description'], id))
        db.commit()
        return jsonify({'message': 'Category updated'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400

@categories_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM categories WHERE id = %s", (id,))
        db.commit()
        return jsonify({'message': 'Category deleted'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    
