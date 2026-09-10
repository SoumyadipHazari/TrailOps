from celery_config import celery
from app import create_app
from models import db, Booking, User,Trek
from email_util import send_email
from datetime import date, timedelta
import csv
import os

app = create_app()
@celery.task
def export_booking_history(user_id):


    with app.app_context():

        bookings = Booking.query.filter_by(
            user_id=user_id
        ).all()

        os.makedirs("exports", exist_ok=True)

        filename = f"exports/booking_history_{user_id}.csv"

        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "User ID",
                "Trek Name",
                "Location",
                "Booking Status",
                "Booking Date",
                "Start Date",
                "End Date"
            ])

            for booking in bookings:
                writer.writerow([
                    booking.user_id,
                    booking.trek.name,
                    booking.trek.location,
                    booking.status,
                    booking.booking_date,
                    booking.trek.start_date,
                    booking.trek.end_date
                ])

        print(f"CSV exported successfully: {filename}")

        user = User.query.get(user_id)

        send_email(
            receiver=user.email,
            subject="Booking History Export Completed",
            body=f"""
            <h2>Your Booking History is Ready</h2>

            <p>Hello <b>{user.name}</b>,</p>

            <p>Your trekking booking history has been exported successfully.</p>

            <p><b>Generated File:</b></p>

            <p>{filename}</p>

            <p>You can now download the generated CSV from the application.</p>

            <br>

            <p>Regards,<br>
            Trekking Management Team</p>
            """
        )

        return filename
    
@celery.task
def daily_trek_reminder():

    with app.app_context():

        tomorrow = date.today() + timedelta(days=1)

        treks = Trek.query.filter_by(
            start_date=tomorrow,
            status="Open"
        ).all()

        if not treks:
            print("No treks starting tomorrow.")
            return

        for trek in treks:

            bookings = Booking.query.filter_by(
                trek_id=trek.id,
                status="Booked"
            ).all()

            for booking in bookings:

                send_email(
                    receiver=booking.user.email,
                    subject=f"Reminder: {trek.name} starts tomorrow!",
                    body=f"""
                    <h2>Trek Reminder</h2>

                    <p>Hello <b>{booking.user.name}</b>,</p>

                    <p>This is a reminder that your trek
                    <b>{trek.name}</b> starts tomorrow.</p>

                    <ul>
                        <li><b>Location:</b> {trek.location}</li>
                        <li><b>Start Date:</b> {trek.start_date}</li>
                        <li><b>End Date:</b> {trek.end_date}</li>
                        <li><b>Difficulty:</b> {trek.difficulty}</li>
                    </ul>

                    <p>Please arrive on time and carry all the necessary trekking equipment.</p>

                    <br>

                    <p>Happy Trekking!</p>

                    <p><b>Trekking Management Team</b></p>
                    """
                )

                print(f"Reminder sent to {booking.user.email}")

        return "Daily reminders completed."
    

@celery.task
def monthly_activity_report():
    with app.app_context():
        completed_treks = Trek.query.filter_by(
            status="Completed"
        ).count()
        participants = (
            db.session.query(Booking.user_id)
            .filter_by(status="Completed")
            .count()
        )
        popular_treks = (
            db.session.query(
                Trek.name,
                db.func.count(Booking.id).label("participants")
            )
            .join(Booking, Booking.trek_id == Trek.id)
            .filter(Booking.status == "Completed")
            .group_by(Trek.id)
            .order_by(db.func.count(Booking.id).desc())
            .limit(5)
            .all()
        )

        admin = User.query.filter_by(role="admin").first()
        if not admin:
            return "No admin found."
        
        if popular_treks:
            popular_html = ""

            for trek, count in popular_treks:
                popular_html += (
                    f"<li><b>{trek}</b> - {count} participants</li>"
                )
        else:
            popular_html = "<p>No completed treks this month.</p>"

        send_email(
            receiver=admin.email,
            subject="Monthly Trekking Activity Report",
            body=f"""
            <h2>Monthly Trekking Activity Report</h2>
            <p>
            <b>Report Month:</b> {date.today().strftime("%B %Y")}
            </p>

            <p>Hello <b>{admin.name}</b>,</p>

            <p>Here is this month's activity summary.</p>

            <ul>
                <li><b>Total Treks Conducted:</b> {completed_treks}</li>
                <li><b>Total Users Participated:</b> {participants}</li>
            </ul>

            <h3>Most Popular Treks</h3>

            <ol>
                {popular_html}
            </ol>

            <br>

            <p>Regards,<br>
            Trekking Management Team</p>
            """
        )
        print(f"Monthly report sent to {admin.email}")
        return "Monthly report sent successfully."