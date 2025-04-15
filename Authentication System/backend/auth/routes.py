from flask import Blueprint, redirect, request, jsonify, url_for
from db import get_db_connection
from utils.password import hash_password, check_password
from utils.jwt_helper import generate_tokens
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.email_service import send_verification_email

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/verify-email/<token>', methods=["GET"])
def verify_email(token):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT user_id, expires_at FROM email_verifications WHERE token=%s", (token,))
    entry = cursor.fetchone()

    if not entry:
        return jsonify({"msg": "Invalid token"}), 400

    if datetime.datetime.utcnow() > entry["expires_at"]:
        return jsonify({"msg": "Token expired"}), 400

    cursor.execute("UPDATE users SET is_verified = TRUE WHERE id=%s", (entry["user_id"],))
    cursor.execute("DELETE FROM email_verifications WHERE token=%s", (token,))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"msg": "Email successfully verified"}), 200

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    password = data["password"]
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        return jsonify({"msg": "User already exists"}), 400

    hashed_pw = hash_password(password).decode("utf-8")
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_pw))

    verify_token = generate_reset_token()
    expiry = token_expiry()
   
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"msg": "User creation failed."}), 500
    user_id = user[0]  # extract actual integer value from tuple

    cursor.execute(
        "INSERT INTO email_verifications (user_id, token, expires_at) VALUES (%s, %s, %s)",
        (user_id, verify_token, expiry)
    )

    verify_link = f"http://localhost:3000/verify-email/{verify_token}"
    send_verification_email(email, verify_link)

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

from utils.token_generator import generate_reset_token, token_expiry
from utils.email_service import send_password_reset_email
import datetime

@auth_bp.route('/request-password-reset', methods=["POST"])
def request_reset():
    email = request.json.get("email")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"msg": "If the email is valid, a reset link will be sent."}), 200

    token = generate_reset_token()
    expiry = token_expiry()
    cursor.execute("INSERT INTO password_resets (user_id, token, expires_at) VALUES (%s, %s, %s)",
                   (user["id"], token, expiry))
    conn.commit()

    reset_link = f"http://localhost:3000/reset-password/{token}"
    send_password_reset_email(email, reset_link)

    cursor.close()
    conn.close()
    return jsonify({"msg": "Reset link sent if email exists."}), 200


@auth_bp.route('/reset-password/<token>', methods=["POST"])
def reset_password(token):
    new_password = request.json.get("password")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT user_id, expires_at FROM password_resets WHERE token=%s", (token,))
    entry = cursor.fetchone()

    if not entry:
        return jsonify({"msg": "Invalid or expired token"}), 400

    if datetime.datetime.utcnow() > entry["expires_at"]:
        return jsonify({"msg": "Token expired"}), 400

    hashed_pw = hash_password(new_password).decode("utf-8")
    cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_pw, entry["user_id"]))
    cursor.execute("DELETE FROM password_resets WHERE token=%s", (token,))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"msg": "Password has been reset successfully"}), 200

# Google:
#   Go to: https://console.cloud.google.com/apis/credentials

#   Create OAuth 2.0 Client ID

#   Authorized redirect URI: http://localhost:5000/login/google/authorized

# GitHub:
#   Go to: https://github.com/settings/developers

#   Register a new OAuth App

#    Homepage: http://localhost:3000

#   Callback: http://localhost:5000/login/github/authorized

from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
import os

# Google OAuth setup
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to="google_login"
)

# GitHub OAuth setup
github_bp = make_github_blueprint(
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    redirect_to="github_login"
)

@auth_bp.route("/google-login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    info = resp.json()
    email = info["email"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (email, password, is_verified) VALUES (%s, %s, %s)", (email, "", True))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

    token = generate_tokens(user["id"])

    return jsonify({"access": token})

@auth_bp.route("/github-login")
def github_login():
    if not github.authorized:
        return redirect(url_for("github.login"))

    resp = github.get("/user")
    info = resp.json()
    email = info.get("email")

    # Fallback: request primary email from GitHub
    if not email:
        email_resp = github.get("/user/emails")
        emails = email_resp.json()
        for e in emails:
            if e.get("primary") and e.get("verified"):
                email = e["email"]
                break

    if not email:
        return jsonify({"msg": "Unable to fetch GitHub email"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (email, password, is_verified) VALUES (%s, %s, %s)", (email, "", True))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

    token = generate_tokens(user["id"])
    return jsonify({"access": token})
