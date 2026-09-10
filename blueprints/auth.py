from flask import Blueprint, request, jsonify
from flask_login import login_user,logout_user, login_required, current_user
from models import db, User
import re

auth_bp = Blueprint("auth", __name__)

ROLE_ADMIN = "admin"
ROLE_STAFF = "staff"
ROLE_USER = "user"

def valid_phone(phone):
    return re.fullmatch(r"\d{10}", phone) is not None


def valid_password(password):
    return len(password) >= 4

@auth_bp.route("/login", methods = ["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({
            "success": True,
            "message": "User already logged in.",
            "role": current_user.role,
            "user": {
                "id": current_user.id,
                "name": current_user.name,
                "email": current_user.email
            }
        }), 200
    

    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is missing."
        }), 400
        
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email = email).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401
                
    if not user.check_password(password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401
        
    if user.status != "active":
        return jsonify({
            "success": False,
            "message": ("Your account has been deactivated by the administrator. "
            "If you believe this is a mistake, please contact "
            "trailops@gmail.com for assistance.")
        }), 403
        
    login_user(user)
    return jsonify({
        "success": True,
        "message": "Login successful.",
        "role": user.role,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200

@auth_bp.route("/register", methods = ["POST"])
def register():
        
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is missing."
        }), 400
    
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if not name or not email or not phone or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400
    
    if not valid_phone(phone):
            return jsonify({
                "success": False,
                "message": "Phone number must contain exactly 10 digits."
            }), 400

    if not valid_password(password):
        return jsonify({
            "success": False,
            "message": "Password must be at least 4 characters long."
        }), 400


    existing_user = User.query.filter_by(email = email).first()
    existing_phone = User.query.filter_by(phone=phone).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already exists."
        }), 409
    
    if existing_phone:
        return jsonify({
            "success": False,
            "message": "Phone no. already exists."
        }), 409

        
    user = User(name = name, email = email, phone = phone, role = ROLE_USER)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "user_id": user.id
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    }), 200


@auth_bp.route("/me", methods=["GET"])
@login_required
def get_current_user():

    return jsonify({
        "success": True,
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role
        }
    }), 200