from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils.password import hash_password, check_password
from utils.jwt_helper import generate_tokens
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods = ["POST"])
def register():
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("select id from users where email = %s", (email,))
    print(cursor.fetchone())
    if cursor.fetchone():
        return jsonify({"msg":"User already exist."}), 400
    
    hashed_pw = hash_password(password).decode("utf-8")
    cursor.execute("Insert into users (email, password) values (%s, %s)", (email, hashed_pw))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"msg": "Registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, password FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user or not check_password(password, user["password"]):
        return jsonify({"msg": "Invalid credentials"}), 401

    tokens = generate_tokens(identity=user["id"])
    return jsonify(tokens), 200

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify({"msg": f"Hello User {user_id}, you're authenticated!"})