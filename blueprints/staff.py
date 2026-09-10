from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Trek, Booking

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/dashboard", methods = ["GET"])
@login_required
def dashboard():

    if current_user.role != "staff":
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403
    
    assigned_treks = Trek.query.filter(
        Trek.staff_id == current_user.id, 
        Trek.status != "Completed"
    ).all()

    total_assigned_treks = len(assigned_treks)
    total_participants = 0
    open_treks = 0
    completed_treks = 0
    pending_treks = 0
    trek_list = []

    for trek in assigned_treks:
        participant_count = Booking.query.filter_by(trek_id = trek.id, status= "Booked").count()

        total_participants += participant_count

        if trek.status == "Pending":
            pending_treks += 1

        if trek.status == "Open":
            open_treks += 1

        trek_list.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "status": trek.status,
            "available_slots": trek.available_slots,
            "participants": participant_count
        })

    return jsonify({
        "success": True,
        "data":{
            "staff_name": current_user.name,
            "total_assigned_treks": total_assigned_treks,
            "total_participants": total_participants,
            "open_treks": open_treks,
            "completed_treks": completed_treks,
            "assigned_treks": trek_list,
            "pending_treks": pending_treks,
        }
    }), 200
    
@staff_bp.route("/treks", methods = ["GET"])
@login_required
def get_assigned_treks():
    if current_user.role != "staff":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403
    
    assigned_treks = Trek.query.filter_by(
        staff_id = current_user.id
    ).order_by(Trek.id.desc()).all()
    
    trek_list = []

    for trek in assigned_treks:
        participant_count = Booking.query.filter_by(
            trek_id = trek.id,
            status = "Booked"
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
            "status": trek.status,
            "participants": participant_count
        })

    return jsonify({
        "success": True,
        "data": trek_list
    }),200

@staff_bp.route("/treks/<int:trek_id>/slots", methods = ["PUT"])
@login_required
def update_slots(trek_id):
    if current_user.role != "staff":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403
    
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({
            "success": False,
            "message": "Trek not found."
        }), 404
    
    if trek.staff_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "You are not assigned to this trek."
        }), 403
    
    if trek.status in ["Inactive","Active", "Completed"]:
        return jsonify({
            "success": False,
            "message": "Slots cannot be changed after the trek has started."
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is missing."
        }), 400
    
    available_slots  = data.get("available_slots")
    if available_slots is None:
        return jsonify({
            "success": False,
            "message": "Available slots are required."
        }), 400
    
    if not isinstance(available_slots, int):
        return jsonify({
            "success": False,
            "message": "Available slots must be an integer."
        }), 400

    if available_slots < 0:
        return jsonify({
            "success": False,
            "message": "Available slots cannot be negative."
        }), 400
    
    trek.available_slots = available_slots

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Available slots updated successfully."
    }), 200

@staff_bp.route("/treks/<int:trek_id>/status", methods=["PUT"])
@login_required
def update_trek_status(trek_id):

    if current_user.role != "staff":
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

    if trek.staff_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "You are not assigned to this trek."
        }), 403
    
    if trek.status == "Inactive":
        return jsonify({
            "success": False,
            "message": "This trek has been deactivated by the admin."
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is missing."
        }), 400

    status = data.get("status")

    if not status:
        return jsonify({
            "success": False,
            "message": "Status is required."
        }), 400

    allowed_status = [
        "Open",
        "Active",
        "Completed"
    ]

    if status not in allowed_status:
        return jsonify({
            "success": False,
            "message": "Invalid trek status."
        }), 400

    status_order = {
        "Pending": 0,
        "Open": 1,
        "Active": 2,
        "Completed": 3
    }

    current = status_order[trek.status]
    new = status_order[status]

    if new != current + 1:
        return jsonify({
            "success": False,
            "message": "Status must follow the correct workflow."
        }), 400
    
    if status == "Open" and trek.available_slots <= 0:
        return jsonify({
            "success": False,
            "message": "Add available slots before opening the trek."
        }), 400

    trek.status = status

    if status == "Completed":
        bookings = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).all()

        for booking in bookings:
            booking.status = "Completed"


    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Trek status updated successfully.",
        "data": {
            "trek_id": trek.id,
            "status": trek.status
        }
    }), 200

@staff_bp.route("/treks/<int:trek_id>/participants", methods = ["GET"])
@login_required
def view_participants(trek_id):

    if current_user.role != "staff":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403
    
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "success": False,
            "message": "Trek not found."
        }), 404
    
    if trek.staff_id != current_user.id:
        return jsonify({
            "success": False,
            "message": "You are not assigned to this trek."
        }), 403
    
    bookings = Booking.query.filter_by(
        trek_id = trek.id,
        status = "Booked"
    ).all()

    participant_list = []

    for booking in bookings:
        participant_list.append({
            "booking_id": booking.id,
            "booking_date": str(booking.booking_date),

            "user":{
                "id": booking.user.id,
                "name": booking.user.name,
                "email": booking.user.email,
                "phone": booking.user.phone
            }
        })

    return jsonify({
        "success": True,
        "trek": {
            "id": trek.id,
            "name": trek.name,
            "location": trek.location
        },
        "total_participants": len(bookings),
        "participants": participant_list
    }), 200