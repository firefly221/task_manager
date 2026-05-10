from flask import Blueprint, jsonify, request

from app.models import Task, db

bp = Blueprint("api", __name__)


@bp.get("/health")
def health():
    return jsonify(status="ok")

@bp.get("/new_route")
def new_route():
    return jsonify(status="added")


@bp.get("/api/tasks")
def list_tasks():
    tasks = Task.query.order_by(Task.id.asc()).all()
    return jsonify([t.as_dict() for t in tasks])


@bp.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="title is required"), 400
    task = Task(title=title, done=False)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.as_dict()), 201


@bp.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(error="not found"), 404
    data = request.get_json(silent=True) or {}
    if "done" in data:
        task.done = bool(data["done"])
    if "title" in data:
        t = (data.get("title") or "").strip()
        if not t:
            return jsonify(error="title cannot be empty"), 400
        task.title = t
    db.session.commit()
    return jsonify(task.as_dict())
