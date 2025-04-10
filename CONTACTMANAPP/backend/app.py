from flask import Flask, request, jsonify
from flask_cors import CORS
import contact_queries as db

app = Flask(__name__)
CORS(app)

@app.route("/contacts", methods = ["GET"])
def get_contacts():
    return jsonify(db.get_all_contacts())

@app.route("/contacts/<int:contact_id>", methods = ["GET"])
def get_contact(contact_id):
    return jsonify(db.get_contact_by_id(contact_id))

@app.route("/contacts", methods = ["POST"])
def add_contact():
    data = request.json
    db.create_contact(data['name'], data['phone'], data['email'], data['address'])
    return jsonify({"msg":"Contact added"}), 201

@app.route('/contacts/<int:contact_id>', methods=['PUT'])
def update(contact_id):
    data = request.json
    db.update_contact(contact_id, data['name'], data['phone'], data['email'], data['address'])
    return jsonify({"message": "Contact updated"})

@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete(contact_id):
    db.delete_contact(contact_id)
    return jsonify({"message": "Contact deleted"})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    return jsonify(db.search_contacts(query))

if __name__ == "__main__":
    app.run(debug=True)