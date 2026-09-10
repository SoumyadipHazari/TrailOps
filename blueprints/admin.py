from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from cache import cache
from datetime import datetime
from models import db, User, Trek, Booking
import re

def valid_phone(phone):
    return re.fullmatch(r"\d{10}", phone) is not None


def valid_password(password):
    return len(password) >= 4

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    total_users = User.query.filter_by(role="user").count()
    total_staff = User.query.filter_by(role="staff").count()
    total_treks = Trek.query.filter(Trek.status != "Completed").count()
    completed_treks = Trek.query.filter_by(status="Completed").count()
    total_bookings = Booking.query.count()

    return jsonify({
        "success": True,
        "data": {
            "total_users": total_users,
            "total_staff": total_staff,
            "total_treks": total_treks,
            "completed_treks": completed_treks,
            "total_bookings": total_bookings
        }
    }), 200

@admin_bp.route("/treks", methods = ["GET"])
@login_required
def get_all_treks():
    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    treks = Trek.query.filter(Trek.status != "Completed").all()
    trek_list = []
    for trek in treks:
        booking_count = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).count()

        trek_list.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "description": trek.description,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date),
            "available_slots": trek.available_slots,
            "booking_count": booking_count,
            "status": trek.status,
            "staff_id": trek.staff_id,
            "staff_name": trek.staff.name if trek.staff else "Not Assigned",
            "created_at": str(trek.created_at)
        })
    
    return jsonify({
        "success": True,
        "data": trek_list
    }), 200

@admin_bp.route("/treks/history", methods=["GET"])
@login_required
def completed_trek_history():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403

    treks = Trek.query.filter_by(
        status="Completed"
    ).order_by(
        Trek.end_date.desc()
    ).all()

    history = []

    for trek in treks:

        participant_count = Booking.query.filter_by(
            trek_id=trek.id,
            status="Completed"
        ).count()

        history.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "description": trek.description,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "status": trek.status,
            "staff": trek.staff.name if trek.staff else "-",
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date),
            "participants": participant_count
        })

    return jsonify({
        "success": True,
        "data": history
    }), 200

@admin_bp.route("/treks", methods = ["POST"])
@login_required
def create_trek():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is missing."
        }), 400
    
    name = data.get("name")
    location = data.get("location")
    difficulty = data.get("difficulty")
    duration = data.get("duration")

    if not data.get("start_date") or not data.get("end_date"):
        return jsonify({
            "success": False,
            "message": "Start date and end date are required."
        }), 400

    start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
    end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()


    if not name or not location:
        return jsonify({
            "success": False,
            "message": "Trek name and location are required."
        }), 400
    
    if difficulty not in ["Easy", "Moderate", "Hard"]:
        return jsonify({
            "success": False,
            "message": "Invalid difficulty level."
        }), 400
    
    if duration is None or duration <= 0:
        return jsonify({
            "success": False,
            "message": "Duration must be greater than zero."
        }), 400
    

    if start_date >= end_date:
        return jsonify({
            "success": False,
            "message": "End date must be after start date."
        }), 400
    
    trek = Trek(
        name = data.get("name"),
        location = data.get("location"),
        description = data.get("description"),
        difficulty = data.get("difficulty"),
        duration = data.get("duration"),
        start_date = start_date,
        end_date = end_date,
        available_slots = 0,
        status = "Pending"
    )

    db.session.add(trek)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Trek created successfully."
    }), 201

@admin_bp.route("/treks/<int:trek_id>", methods = ["PUT"])
@login_required

def update_trek(trek_id):
    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "success": False,
            "message": "Trek not found."
        }), 404
    
    data = request.get_json()

    if data.get("name"):
        trek.name = data.get("name")

    if data.get("location"):
        trek.location = data.get("location")

    if data.get("description"):
        trek.description = data.get("description")
    
    if data.get("difficulty"):
        if data["difficulty"] not in ["Easy", "Moderate", "Hard"]:
            return jsonify({
                "success": False,
                "message": "Invalid difficulty level."
            }), 400
        trek.difficulty = data.get("difficulty")

    if data.get("duration"):
        if data["duration"] <= 0:
            return jsonify({
                "success": False,
                "message": "Duration must be greater than zero."
            }), 400
        trek.duration = data.get("duration")

    if data.get("start_date"):
        trek.start_date = datetime.strptime(
            data.get("start_date"), "%Y-%m-%d"
        ).date()

    if data.get("end_date"):
        trek.end_date = datetime.strptime(
            data.get("end_date"), "%Y-%m-%d"
        ).date()

    if trek.start_date >= trek.end_date:
        return jsonify({
            "success": False,
            "message": "End date must be after start date."
        }), 400

    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Trek updated successfully"
    }), 200

@admin_bp.route("/treks/<int:trek_id>/toggle", methods=["PUT"])
@login_required
def toggle_trek(trek_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }),403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "success": False,
            "message": "Trek not found."
        }),404

    if trek.status in ["Open", "Active", "Completed"]:
        return jsonify({
            "success": False,
            "message": "Operational treks cannot be deactivated."
        }), 400

    if trek.status == "Pending":
        trek.status = "Inactive"
    elif trek.status == "Inactive":
        trek.status = "Pending"

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Trek status updated successfully."
    }),200


@admin_bp.route("/staff", methods = ["GET"])
@login_required
@cache.memoize(timeout=300)
def get_all_staff():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access Denied."
        }), 403
    
    staff_members = User.query.filter_by(role="staff").all()
    staff_list = []

    for staff in staff_members:
        staff_list.append({
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
            "phone": staff.phone,
            "experience": staff.experience,
            "status": staff.status,
            "created_at": str(staff.created_at)
        })

    return jsonify({
        "success": True,
        "data": staff_list
    }), 200

@admin_bp.route("/staff/active", methods=["GET"])
@login_required
@cache.memoize(timeout=300)
def get_active_staff():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403

    staff_members = User.query.filter_by(
        role="staff",
        status="active"
    ).all()

    staff_list = []

    for staff in staff_members:

        staff_list.append({
            "id": staff.id,
            "name": staff.name
        })

    return jsonify({
        "success": True,
        "data": staff_list
    }), 200

@admin_bp.route("/staff", methods = ["POST"])
@login_required
def create_staff():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    data  = request.get_json()

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
            "message": "all the fields are required."
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
    
    existing_staff = User.query.filter_by(email = email).first()

    if existing_staff:
        return jsonify({
            "success": False,
            "message": "email already exists."
        }), 400
    
    existing_phone = User.query.filter_by(phone = phone).first()

    if existing_phone:
        return jsonify({
            "success": False,
            "message": "phone no. already exists."
        }), 400
    
    staff = User(
        name = name,
        email = email,
        phone = phone,
        role = "staff",
        experience = data.get("experience"),
    )

    staff.set_password(password)

    db.session.add(staff)
    db.session.commit()
    cache.delete_memoized(get_all_staff)
    cache.delete_memoized(get_active_staff)

    return jsonify({
        "success": True,
        "message": "Staff created successfully."
    }), 201

@admin_bp.route("/staff/<int:staff_id>", methods = ["PUT"])
@login_required
def update_staff(staff_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    staff = User.query.filter_by(id = staff_id, role = "staff").first()

    if not staff:
        return jsonify({
            "success": False,
            "message": "Staff not found."
        }), 404
    
    data = request.get_json()

    if data.get("name"):
        staff.name = data.get("name")

    if data.get("phone"):

        if not valid_phone(data.get("phone")):
            return jsonify({
                "success": False,
                "message": "Phone number must contain exactly 10 digits."
            }), 400

        existing_phone = User.query.filter(User.phone == data.get("phone"), User.id != staff.id).first()
        if existing_phone:
            return jsonify({
                "success": False,
                "message": "phone no. already exists."
            }), 400

        staff.phone = data.get("phone")

    if data.get("experience") is not None:
        staff.experience = data.get("experience")

    if data.get("password"):
        if not valid_password(data.get("password")):
            return jsonify({
                "success": False,
                "message": "Password must be at least 4 characters long."
            }), 400
        staff.set_password(data.get("password"))

    if data.get("status"):
        if data["status"] not in ["active", "inactive"]:
            return jsonify({
                "success": False,
                "message": "Invalid status."
            }), 400
        
        staff.status = data.get("status")

    db.session.commit()
    cache.delete_memoized(get_all_staff)
    cache.delete_memoized(get_active_staff)

    return jsonify({
        "success": True,
        "message": "staff updated successfully."
    }), 200

@admin_bp.route("/treks/<int:trek_id>/assign-staff", methods = ["PUT"])
@login_required
def assign_staff(trek_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "success": False,
            "message": "Trek not found."
        }), 404
    
    data = request.get_json()

    if not data: 
        return jsonify({
            "success": False,
            "message": "Request body is missing"
        }), 400
    
    staff_id = data.get("staff_id")

    if staff_id in [None, ""]:
        trek.staff_id = None
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Staff removed successfully."
        }), 200
    
    staff = User.query.filter_by(
        id = staff_id,
        role = "staff"
    ).first()

    if not staff:
        return jsonify({
            "success": False,
            "message": "staff account is inactive"
        }), 400
    
    if staff.status != "active":
        return jsonify({
            "success": False,
            "message": "Staff account is inactive"
        }), 400
    
    if trek.status != "Pending":
        return jsonify({
            "success": False,
            "message": "Staff can only be assigned to pending treks."
        }), 400
    
    trek.staff_id = staff.id

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Staff assigned successfully",
        "data": {
            "trek_id": trek.id,
            "trek_name": trek.name,
            "staff_id": staff.id,
            "staff_name": staff.name
        }
    }), 200


@admin_bp.route("/users", methods = ["GET"])
@login_required
def get_all_users():
    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    users = User.query.filter_by(role = "user").all()

    user_list = []

    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "status": user.status,
            "created_at": str(user.created_at)
        })

    return jsonify({
        "success": True,
        "data": user_list
    }), 200


@admin_bp.route("/users/<int:user_id>/status", methods = ["PUT"])
@login_required
def deactivate_user(user_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403

    user = User.query.filter_by(
        id=user_id,
        role="user"
    ).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    data = request.get_json()

    status = data.get("status")

    if status not in ["active", "inactive"]:
        return jsonify({
            "success": False,
            "message": "Invalid status."
        }), 400

    user.status = status

    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"User {status} successfully."
    }), 200

@admin_bp.route("/search", methods = ["GET"])
@login_required
def universal_search():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    query = request.args.get("q")

    if not query:
        return jsonify({
            "success": False,
            "message": "Search query is required."
        }), 400
    
    users = User.query.filter(
        User.role == "user",
        (
            User.name.ilike(f"%{query}%") |
            User.email.ilike(f"%{query}%") |
            User.phone.ilike(f"%{query}%")
        )
    ).all()

    staff = User.query.filter(
        User.role == "staff",
        (
            User.name.ilike(f"%{query}%") |
            User.email.ilike(f"%{query}%") |
            User.phone.ilike(f"%{query}%")
        )
    ).all()

    treks = Trek.query.filter(
        Trek.name.ilike(f"%{query}%") |
        Trek.location.ilike(f"%{query}%") |
        Trek.description.ilike(f"%{query}%")
    ).all()

    user_list = []
    staff_list = []
    trek_list = []
    
    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "status": user.status
        })

    for member in staff:
        staff_list.append({
            "id": member.id,
            "name": member.name,
            "email": member.email,
            "phone": member.phone,
            "status": member.status
        })

    for trek in treks:
        trek_list.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "status": trek.status
        })

    return jsonify({
        "success": True,
        "data":{
            "users": user_list,
            "staff": staff_list,
            "treks": trek_list
        }
    }), 200

@admin_bp.route("/bookings", methods = ["GET"])
@login_required
def get_all_bookings():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    bookings = Booking.query.all()
    booking_list = []

    for booking in bookings:
        booking_list.append({
            "booking_id": booking.id,
            "booking_date": str(booking.booking_date),
            "booking_status": booking.status,

            "user": {
                "id": booking.user.id,
                "name": booking.user.name,
                "email": booking.user.email
            },
            "trek":{
                "id": booking.trek.id,
                "name": booking.trek.name,
                "location": booking.trek.location,
                "status": booking.trek.status
            }

        })

    return jsonify({
        "success": True,
        "data": booking_list
    }), 200

@admin_bp.route("/send-reminders", methods=["POST"])
@login_required
def send_daily_reminders():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403

    from tasks import daily_trek_reminder

    daily_trek_reminder.delay()

    return jsonify({
        "success": True,
        "message": "Daily reminder job has been started."
    }), 202

@admin_bp.route("/generate-monthly-report", methods=["POST"])
@login_required
def generate_monthly_report():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403

    from tasks import monthly_activity_report

    monthly_activity_report.delay()

    return jsonify({
        "success": True,
        "message": "Monthly activity report generation started."
    }), 202