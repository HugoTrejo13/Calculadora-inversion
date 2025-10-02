from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

# Inicialización de la app
app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = 'super-secret-key'  # cámbiala en producción
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de DB y JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)

# --------------------
# MODELO DE USUARIO
# --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Crear tablas (si no existen)
with app.app_context():
    db.create_all()

# --------------------
# RUTAS
# --------------------

@app.route("/")
def home():
    return {"message": "Servidor Flask corriendo correctamente 🚀"}

# Registro de usuario
@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado correctamente ✅"}), 201

# Login de usuario
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"token": access_token}), 200

# Ruta protegida de ejemplo
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": "Accediste a una ruta protegida 🔒"})


# --------------------
# MAIN
# --------------------
if __name__ == "__main__":
    app.run(debug=True)

