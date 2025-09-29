from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Tabla Users
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum("student", "admin", name="user_roles"), nullable=False, default="student")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    listings = db.relationship("Listing", backref="seller", lazy=True)
    favorites = db.relationship("Favorite", backref="user", lazy=True)
    messages_sent = db.relationship("Message", foreign_keys="Message.from_user_id", backref="from_user", lazy=True)
    messages_received = db.relationship("Message", foreign_keys="Message.to_user_id", backref="to_user", lazy=True)
    orders_bought = db.relationship("Order", foreign_keys="Order.buyer_id", backref="buyer", lazy=True)
    orders_sold = db.relationship("Order", foreign_keys="Order.seller_id", backref="seller", lazy=True)


# Tabla Listings
class Listing(db.Model):
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum("product", "service", name="listing_types"), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum("active", "paused", "sold", name="listing_status"), nullable=False, default="active")
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    favorites = db.relationship("Favorite", backref="listing", lazy=True)
    messages = db.relationship("Message", backref="listing", lazy=True)
    orders = db.relationship("Order", backref="listing", lazy=True)


# Tabla Favorites
class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Tabla Messages
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"), nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Tabla Orders
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.Enum("initiated", "confirmed", "cancelled", "completed", name="order_status"), nullable=False, default="initiated")
    agreed_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
