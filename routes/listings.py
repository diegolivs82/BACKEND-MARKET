from flask import Blueprint, request, jsonify
from models.models import db, Listing

listings_bp = Blueprint("listings", __name__)

# GET /listings -> lista todos los listings
@listings_bp.get("/")
def list_listings():
    listings = Listing.query.order_by(Listing.created_at.desc()).all()
    return jsonify([
        {
            "id": l.id,
            "title": l.title,
            "description": l.description,
            "type": l.type,
            "price": float(l.price),
            "category": l.category,
            "status": l.status,
            "seller_id": l.seller_id,
            "created_at": l.created_at.isoformat()
        }
        for l in listings
    ]), 200

# POST /listings -> crear un nuevo listing
@listings_bp.post("/")
def create_listing():
    data = request.get_json() or {}
    required = ["title", "description", "type", "price", "category", "seller_id"]
    missing = [f for f in required if f not in data]
    if missing:
        return {"error": f"Faltan campos: {', '.join(missing)}"}, 400

    new_listing = Listing(
        title=data["title"],
        description=data["description"],
        type=data["type"],      # "product" o "service"
        price=data["price"],
        category=data["category"],
        seller_id=data["seller_id"],
    )
    db.session.add(new_listing)
    db.session.commit()
    return {"ok": True, "id": new_listing.id}, 201
# GET /listings/<id> -> detalle
@listings_bp.get("/<int:listing_id>")
def get_listing(listing_id):
    l = Listing.query.get_or_404(listing_id)
    return {
        "id": l.id,
        "title": l.title,
        "description": l.description,
        "type": l.type,
        "price": float(l.price),
        "category": l.category,
        "status": l.status,
        "seller_id": l.seller_id,
        "created_at": l.created_at.isoformat()
    }, 200

# PUT /listings/<id> -> actualizar campos
@listings_bp.put("/<int:listing_id>")
def update_listing(listing_id):
    l = Listing.query.get_or_404(listing_id)
    data = request.get_json() or {}
    for field in ["title", "description", "type", "price", "category", "status"]:
        if field in data:
            setattr(l, field, data[field])
    db.session.commit()
    return {"ok": True}, 200

# DELETE /listings/<id> -> borrar
@listings_bp.delete("/<int:listing_id>")
def delete_listing(listing_id):
    l = Listing.query.get_or_404(listing_id)
    db.session.delete(l)
    db.session.commit()
    return {"ok": True}, 200



