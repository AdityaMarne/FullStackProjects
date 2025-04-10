from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import mysql

comments_bp = Blueprint('comments', __name__)

comments_bp.route('/add', methods = ['POST'])
@jwt_required
def add_comment():
    data = request.get_json()
    user_id = get_jwt_identity()
    blog_id = data['blog_id']
    content = data['content']

    cur = mysql.connection.cursor()
    cur.execute("select id from blog_posts where id = %s",(blog_id))
    blog = cur.fetchone()

    if not blog:
        return jsonify({"message":"Blog post not found"}), 404
    
    cur.execute("INSERT INTO comments (blog_id, user_id, content) VALUES (%s, %s, %s)",
                (blog_id, user_id, content))
    cur.commit()
    cur.cloe()

    return jsonify({"message": "Comment added successfully"}), 201

@comments_bp.route("/<int:blog_id>", methods = ['GET'])
def get_comments(blog_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT c.id, c.content, u.username, c.created_at FROM comments c JOIN users u ON c.user_id = u.id WHERE c.blog_id = %s ORDER BY c.created_at DESC", 
                (blog_id,))
    comments = cur.fetchall()
    cur.close()

    comments_list = [{"id": c[0], "content": c[1], "author": c[2], "created_at": c[3]} for c in comments]
    return jsonify(comments_list), 200

@comments_bp.route("/update/<int:comment_id>", methods = ['PUT'])
@jwt_required
def update_comment(comment_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    new_content = data['content']

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM comments WHERE id = %s", (comment_id,))
    comment = cur.fetchone()

    if not comment:
        return jsonify({"message":"Comment not found"}), 404
    
    if comment[0] != user_id:
        return jsonify({"message": "Unauthorized"}), 403
    
    cur.execute("UPDATE comments SET content = %s WHERE id = %s", (new_content, comment_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Comment updated successfully"}), 200


@comments_bp.route('/delete/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM comments WHERE id = %s", (comment_id,))
    comment = cur.fetchone()

    if not comment:
        return jsonify({"message": "Comment not found"}), 404

    if comment[0] != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    cur.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Comment deleted successfully"}), 200




