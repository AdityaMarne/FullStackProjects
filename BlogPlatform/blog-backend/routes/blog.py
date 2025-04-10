from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import markdown
from db import mysql

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/create', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    print(f"Received data: {data}")  # Check the incoming data
    user_id = get_jwt_identity()
    print(f"User ID from token: {user_id}")  # Check the identity retrieved from the token
    title = data['title']
    content = data['content']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO blog_posts (user_id, title, content) VALUES (%s, %s, %s)",
                (user_id, title, content))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Blog post created successfully"}), 201

@blog_bp.route('/all', methods=['GET'])
def get_all_posts():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.id, b.title, b.content, u.username, b.created_at, b.is_featured
        FROM blog_posts b JOIN users u ON b.user_id = u.id
        ORDER BY b.created_at DESC
    """)
    posts = cur.fetchall()

    posts_list = []
    for post in posts:
        cur.execute("""
            SELECT t.name FROM tags t 
            JOIN blog_post_tags bpt ON t.id = bpt.tag_id 
            WHERE bpt.blog_id = %s
        """, (post[0],))
        tags = [t[0] for t in cur.fetchall()]

        posts_list.append({
            "id": post[0],
            "title": post[1],
            "content": markdown.markdown(post[2]),  # Convert Markdown to HTML
            "author": post[3],
            "created_at": post[4],
            "is_featured": post[5],
            "tags": tags
        })

    cur.close()
    return jsonify(posts_list), 200
    
@blog_bp.route("/<int:post_id>", methods=['GET'])
def get_post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT b.id, b.title, b.content, u.username, b.created_at FROM blog_posts b JOIN users u ON b.user_id = u.id WHERE b.id = %s", (post_id,))
    post = cur.fetchone()
    cur.close()

    if not post:
        return jsonify({"message": "Post not found"}), 404
    
    post_data = {"id": post[0], "title": post[1], "content": post[2], "author": post[3], "created_at": post[4]}
    return jsonify(post_data), 200

@blog_bp.route("/update/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    title = data.get('title')
    content = data.get('content')

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM blog_posts WHERE id = %s", (post_id,))
    post = cur.fetchone()

    if not post:
        return jsonify({"message": "Post not found"}), 404
    
    if post[0] != user_id:  # Check if the logged-in user is the author
        return jsonify({"message": "Unauthorized"}), 403
    
    cur.execute("UPDATE blog_posts SET title = %s, content = %s WHERE id = %s",
                (title, content, post_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Blog post updated successfully"}), 200

@blog_bp.route('/delete/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM blog_posts WHERE id = %s", (post_id,))
    post = cur.fetchone()

    if not post:
        return jsonify({"message": "Post not found"}), 404

    if post[0] != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    cur.execute("DELETE FROM blog_posts WHERE id = %s", (post_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Blog post deleted successfully"}), 200

@blog_bp.route('/feature/<int:post_id>', methods=['PUT'])
@jwt_required()
def feature_post(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM blog_posts WHERE id = %s", (post_id,))
    post = cur.fetchone()

    if not post:
        return jsonify({"message": "Post not found"}), 404

    cur.execute("UPDATE blog_posts SET is_featured = TRUE WHERE id = %s", (post_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Blog post marked as featured"}), 200

@blog_bp.route('/featured', methods=['GET'])
def get_featured_posts():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT b.id, b.title, b.content, u.username, b.created_at
        FROM blog_posts b JOIN users u ON b.user_id = u.id
        WHERE b.is_featured = TRUE
        ORDER BY b.created_at DESC
    """)
    posts = cur.fetchall()

    posts_list = [{"id": p[0], "title": p[1], "content": p[2], "author": p[3], "created_at": p[4]} for p in posts]
    cur.close()
    return jsonify(posts_list), 200
