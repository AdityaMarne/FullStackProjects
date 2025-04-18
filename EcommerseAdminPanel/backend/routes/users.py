from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from db import get_db_connection

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = generate_password_hash(data['password'])
    role = data.get('role', 'user') #default is user

    if not name or not email or not password:
        return jsonify({"error":"Fields are required."})

    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user  = cursor.fetchone()

        if existing_user :
            return jsonify({"msg":"Your are alrady registered. please login"})
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    try:
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                       (name, email, password, role))
        db.commit()
        return jsonify({"msg":"User registered successfully"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error':str(e)}), 400
    
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    if not email or not password:
        return jsonify({"error":"Fields are required"})
    
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity={'id': str(user['id']), 'role': user['role']})
        return jsonify({'token': access_token, 'user': {'id': user['id'], 'name': user['name'], 'role': user['role']}})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

