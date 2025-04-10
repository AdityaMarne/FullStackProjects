from flask import Blueprint, request, jsonify
from db import mysql, app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt(app)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods = ['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", 
                (username, email, password))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message":"User registered successfully"}), 201

@auth_bp.route("/login", methods = ['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user[1], password):
        access_token = create_access_token(identity = user[0])
        #access_token = create_access_token(identity=str(user_id))  # Ensure 'sub' is a string #Optional
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401