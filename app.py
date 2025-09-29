from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os 
from routes.listings import listings_bp
from routes.users import users_bp



# 1) Cargar variables del .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 2) Crear la app y configurar SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Agrega esta línea:
app.url_map.strict_slashes = False

# 3) Importar db y modelos y “enganchar” la app
from models.models import db, User, Listing, Favorite, Message, Order  # noqa: E402
db.init_app(app)
# Registrar blueprint de listings
app.register_blueprint(listings_bp, url_prefix="/listings")
app.register_blueprint(users_bp,    url_prefix="/users")


# 4) Crear tablas si no existen
with app.app_context():
    db.create_all()

# 5) Rutas simples de prueba
@app.get("/")
def home():
    return "✅ Flask está funcionando y conectado a la base de datos"

@app.get("/health")
def health():
    try:
        # ping simple a la BD
        db.session.execute(db.text("SELECT 1"))
        return {"ok": True, "db": "up"}
    except Exception as e:
        return {"ok": False, "db": "down", "error": str(e)}, 500

# 6) Ruta semilla para crear un usuario demo
@app.post("/seed-user")
def seed_user():
    email = "demo@mayab.mx"
    u = User.query.filter_by(email=email).first()
    if not u:
        u = User(name="Usuario Demo", email=email, role="student")
        db.session.add(u)
        db.session.commit()
    return {"ok": True, "user_id": u.id}

if __name__ == "__main__":
    app.run(debug=True)


