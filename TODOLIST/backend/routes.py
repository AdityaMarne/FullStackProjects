from flask import Blueprint, request, jsonify
from models import db, Task

api = Blueprint('api', __name__)

@api.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": task.id, "title": task.title, "completed": task.completed}
        for task in tasks
    ])


@api.route("/tasks", methods = ["POST"])
def add_task():
    data = request.json
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added!"})

@api.route("/tasks/<int:id>", methods = ["PUT"])
def update_task(id):
    task = Task.query.get(id)
    data = request.json
    task.compeletd = data['completed']
    db.session.commit()
    return jsonify({"msg" : "Task updated"})

@api.route("/tasks/<int:id>", methods = ['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg":"Task deleted"})

