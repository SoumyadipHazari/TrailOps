from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id  = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), unique = True, nullable = False, index = True)
    password_hash = db.Column(db.String(255), nullable = False)
    phone = db.Column(db.String(50), nullable = False)
    
    role = db.Column(db.String(30), nullable = False, default = "user")
    status = db.Column(db.String(30), nullable = False, default = "active") 
    experience = db.Column (db.Integer)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    assigned_treks = db.relationship("Trek", backref = "staff", lazy = True)

    bookings = db.relationship("Booking", backref = "user", lazy = True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.email}>"


class Trek(db.Model):
    __tablename__  = "treks"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    location = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(30), nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    available_slots = db.Column(db.Integer, nullable = False, default = 0)
    status = db.Column(db.String(40), nullable = False, default = "Pending")
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    
    bookings = db.relationship("Booking", backref = "trek", lazy = True)

    def __repr__(self):
        return f"<Trek {self.name}>"
    

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable = False)
    booking_date = db.Column(db.DateTime, default = datetime.utcnow)
    status = db.Column(db.String(30), default = "Booked", nullable = False)

    __table_args__ = (db.UniqueConstraint("user_id", "trek_id", name = "unique_booking"),)

    def __repr__(self):
        return f"<Booking User:{self.user_id} Trek:{self.trek_id}>"