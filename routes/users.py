from flask import Blueprint, request, jsonify
from models.models import db, User

users_bp = Blueprint("users", __name__)

# GET /users  y /users/
@users_bp.route("", methods=["GET"])
@users_bp.route("/", methods=["GET"])
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([
        {"id": u.id, "name": u.name, "email": u.email, "role": u.role}
        for u in users
    ]), 200

# POST /users  y /users/
@users_bp.route("", methods=["POST"])
@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    for field in ["name", "email", "role"]:
        if field not in data:
            return {"error": f"Falta {field}"}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "Email ya registrado"}, 409

    u = User(name=data["name"], email=data["email"], role=data["role"])
    db.session.add(u)
    db.session.commit()
    return {"ok": True, "id": u.id}, 201
# GET /users/<id> -> detalle
@users_bp.get("/<int:user_id>")
def get_user(user_id):
    u = User.query.get_or_404(user_id)
    return {
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "role": u.role,
        "created_at": u.created_at.isoformat()
    }, 200

# PUT /users/<id> -> actualizar (name, role)
@users_bp.put("/<int:user_id>")
def update_user(user_id):
    u = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    for field in ["name", "role"]:
        if field in data:
            setattr(u, field, data[field])
    db.session.commit()
    return {"ok": True}, 200

# DELETE /users/<id> -> borrar
@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    return {"ok": True}, 200




