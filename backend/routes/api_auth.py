from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import SessionLocal, User

api_auth_bp = Blueprint("api_auth", __name__)

@api_auth_bp.route("/api/auth/register", methods=["POST"])
def api_register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    with SessionLocal() as db:
        if db.query(User).filter_by(email=email).first():
            return jsonify({"msg": "Email already registered"}), 409

        user = User(email=email, password_hash=generate_password_hash(password))
        db.add(user)
        db.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@api_auth_bp.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    with SessionLocal() as db:
        user = db.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            token = create_access_token(identity=email)
            return jsonify(access_token=token), 200
        else:
            return jsonify({"msg": "Invalid credentials"}), 401


@api_auth_bp.route("/api/auth/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
