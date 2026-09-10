from flask import Blueprint, request, jsonify, send_from_directory
from flask_login import login_required, current_user
from datetime import datetime
from models import db, User, Trek, Booking
import os,re

user_bp = Blueprint("user", __name__)

def valid_phone(phone):
    return re.fullmatch(r"\d{10}", phone) is not None


def valid_password(password):
    return len(password) >= 4

@user_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():

    if current_user.role != "user":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403

    return jsonify({
        "success": True,
        "data": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "phone": current_user.phone
        }
    }), 200

@user_bp.route("/dashboard", methods = ["GET"])
@login_required
def dashboard():

    if current_user.role != "user":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    total_bookings = Booking.query.filter_by(user_id = current_user.id).count()
    active_bookings = Booking.query.filter_by(user_id = current_user.id, status = "Booked").count()
    completed_treks = Booking.query.filter_by(user_id = current_user.id, status = "Completed").count()
    cancelled_bookings = Booking.query.filter_by(user_id = current_user.id, status = "Cancelled").count()
    completed_history = Booking.query.filter_by(
        user_id=current_user.id,
        status="Completed"
    ).order_by(
        Booking.booking_date.desc()
    ).limit(5).all()

    history = []

    for booking in completed_history:
        history.append({
            "trek_name": booking.trek.name,
            "location": booking.trek.location,
            "difficulty": booking.trek.difficulty,
            "duration": booking.trek.duration,
            "completed_date": str(booking.trek.end_date)
        })

    return jsonify({
        "success": True,
        "data": {
            "user_name": current_user.name,
            "total_bookings": total_bookings,
            "active_bookings": active_bookings,
            "completed_treks": completed_treks,
            "cancelled_bookings": cancelled_bookings,
            "history": history
        }
    }), 200

@user_bp.route("/treks", methods = ["GET"])
@login_required
def get_available_treks():

    if current_user.role != "user":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    available_treks = Trek.query.filter(Trek.status.in_(["Open", "Active"])).all()
    trek_list = []
    for trek in available_treks:
        already_booked = Booking.query.filter(
            Booking.user_id == current_user.id,
            Booking.trek_id == trek.id,
            Booking.status != "Cancelled"
        ).first() is not None

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
            "status": trek.status,
            "staff": trek.staff.name if trek.staff else None,
            "already_booked": already_booked
        })

    return jsonify({
        "success": True,
        "data": trek_list
    }), 200

@user_bp.route("/bookings", methods = ["POST"])
@login_required
def book_trek():
    if current_user.role != "user":
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
    
    trek_id = data.get("trek_id")

    if trek_id is None:
        return jsonify({
            "success": False,
            "message": "Trek ID is required"
        }), 400
    
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({
            "success": False,
            "message": "Trek not found"
        }), 404
    
    if trek.status != "Open":
        return jsonify({
            "success": False,
            "message": "This trek is not open for booking."
        }), 400
    
    if trek.available_slots <= 0:
        return jsonify({
            "success": False,
            "message": "No slots available for booking."
        }), 400

    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id
    ).first()

    if existing_booking:

        if existing_booking.status == "Booked":
            return jsonify({
                "success": False,
                "message": "You have already booked this trek."
            }), 409

        if existing_booking.status == "Cancelled":
            existing_booking.status = "Booked"
            existing_booking.booking_date = datetime.utcnow()
            trek.available_slots -= 1

            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Trek booked successfully.",
                "booking_id": existing_booking.id
            }), 200

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id,
        status="Booked"
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Trek booked successfully",
        "booking_id": booking.id
    }), 201

@user_bp.route("/bookings", methods = ["GET"])
@login_required
def booking_history():

    if current_user.role != "user":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    bookings = Booking.query.filter_by(user_id = current_user.id).order_by(Booking.booking_date.desc()).all()

    booking_list = []
    for booking in bookings:
        booking_list.append({
            "booking_id": booking.id,
            "booking_date": str(booking.booking_date),
            "booking_status": booking.status,

            "trek": {
                "id": booking.trek.id,
                "name": booking.trek.name,
                "location": booking.trek.location,
                "difficulty": booking.trek.difficulty,
                "duration": booking.trek.duration,
                "start_date": str(booking.trek.start_date),
                "end_date": str(booking.trek.end_date),
                "status": booking.trek.status
            }
        })

    return jsonify({
        "success": True,
        "total_bookings": len(booking_list),
        "data": booking_list
    }), 200

@user_bp.route("/export-bookings", methods=["POST"])
@login_required
def export_bookings():

    if current_user.role != "user":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    from tasks import export_booking_history
    export_booking_history.delay(current_user.id)

    return jsonify({
        "success": True,
        "message": "Booking history export has started. Your CSV will be generated shortly."
    }), 202

@user_bp.route("/download-bookings", methods=["GET"])
@login_required
def download_bookings():

    if current_user.role != "user":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403

    filename = f"booking_history_{current_user.id}.csv"

    export_folder = os.path.join(os.getcwd(), "exports")

    file_path = os.path.join(export_folder, filename)

    if not os.path.exists(file_path):
        return jsonify({
            "success": False,
            "message": "No exported booking history found. Please export your booking history first."
        }), 404

    return send_from_directory(
        directory=export_folder,
        path=filename,
        as_attachment=True
    )

@user_bp.route("/bookings/<int:booking_id>/cancel", methods = ["PUT"])
@login_required
def cancel_booking(booking_id):

    if current_user.role != "user":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({
            "success": False,
            "message": "Booking not found"
        }), 404
    
    if booking.user_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "You are not authorized to cancel the booking."
        }), 403
    
    if booking.status != "Booked":
        return jsonify({
            "success": False,
            "message": "only active bookings can be cancelled"
        }),400
    
    if booking.trek.status in ["Active", "Completed"]:
        return jsonify({
            "success": False,
            "message": "This trek has already started and cannot be cancelled."
        }), 400
    
    booking.status = "Cancelled"
    booking.trek.available_slots += 1

    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Booking cancelled successfully"
    }), 200


@user_bp.route("/profile", methods = ["PUT"])
@login_required
def profile_update():

    if current_user.role != "user":
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
    
    if data.get("name"):
        current_user.name = data.get("name")
    
    if data.get("phone"):
        phone = data.get("phone")
        if not valid_phone(phone):
            return jsonify({
                "success": False,
                "message": "Phone number must contain exactly 10 digits."
            }), 400

        existing_phone = User.query.filter_by(phone = data.get("phone")).first()

        if existing_phone and existing_phone.id != current_user.id:
            return jsonify({
                "success": False,
                "message": "Phone number already exists."
            }), 409
    
        current_user.phone = phone

    if data.get("password"):
        password = data.get("password")
        if not valid_password(password):
            return jsonify({
                "success": False,
                "message": "Password must be at least 4 characters long."
            }),400

        current_user.set_password(password)

    db.session.commit()

    return jsonify({
        "success":  True,
        "message": "Profile updated successfully."
    }),200

