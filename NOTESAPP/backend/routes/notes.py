from flask import Blueprint, request, jsonify
from db import get_db_connection

notes_db = Blueprint('notes', __name__)

@notes_db.route("/notes")

@notes_db.route("/notes", methods = ["GET"])
def get_notes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return jsonify(notes)

@notes_db.route("/notes", methods = ["POST"])
def create_note():
    data = request.json
    title = data['title']
    content = data['content']
    color = data.get("color", "#ffffff")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (title, content, color) VALUES (%s, %s, %s)', (title, content, color))
    conn.commit()
    conn.close()
    return jsonify({"msg":"Note created"}), 201

@notes_db.route("/notes/<int:note_id>", methods = ["PUT"])
def update_note(note_id):
    data = request.json
    title = data['title']
    content = data['content']
    color = data.get("color", '#ffffff')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE notes SET title=%s, content=%s, color=%s WHERE id=%s', (title, content, color, note_id))
    conn.commit()
    conn.close()
    return jsonify({"msg":"Notes updated"})

@notes_db.route("/notes/<int:note_id>", methods = ["DELETE"])
def delete_note(note_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id=%s', (note_id,))
    conn.commit()
    conn.close()
    return jsonify({'msg': 'Note deleted'})


