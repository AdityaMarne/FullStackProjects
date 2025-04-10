from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import mysql

tags_bp = Blueprint('tags', __name__)

@tags_bp.route('/create', methods=['POST'])
@jwt_required()
def create_tag():
    data = request.get_json()
    tag_name = data['name']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tags (name) VALUES (%s) ON DUPLICATE KEY UPDATE name = name", (tag_name,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Tag added successfully"}), 201

@tags_bp.route('/all', methods=['GET'])
def get_tags():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tags")
    tags = cur.fetchall()
    cur.close()

    tags_list = [{"id": t[0], "name": t[1]} for t in tags]
    return jsonify(tags_list), 200
