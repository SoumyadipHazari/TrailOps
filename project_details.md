# Trekking Management Application - V2

A Trekking Management Application web application that allows Admin, Trek Staff and Users (Trekkers) to interact with the system based on their roles.

## Frameworks -

- Flask for API
- VueJS for UI
- VueJS Advanced with CLI (only if required)
- Jinja 2 templates if using CDN only for entry point (not to be used for UI)
- Bootstrap for HTML generation and styling (no other CSS framework is allowed)
- SQLite for database (no other database is permitted)
- Redis for caching 
- Redis and Celery for batch jobs

## Roles and Functionalities - 

1. *Admin*

Admin is the pre-existing superuser of the application.

- Can create, update and remove trekking routes
- Can add and manage trek staff
- Can assign staff to treks
- Can view and manage all users, staff, and treks
- Can search users, staff, or treks
- Can deactivate or blacklist users or staff
- Can view reports and trekking statistics.

2. *Trek Staff*

- Can log in only after being created by Admin
- Can view assigned treks by admin
- Can manage trek details such as:
  - Available slots
  - Trek status (Open / Closed)
- Can view list of registered users for their treks
- Can update trek completion status

3. *User (Trekker)*

- Can register, log in, and update their profile
- Can view approved/open treks
- Can search and filter treks based on difficulty, location, and duration
- Can book treks
- Can view booking status and trekking history

### Key terminologies

1. *Admin*: A user with the highest level of access who manages the entire trekking system.
2. *Trek Staff*: A staff member responsible for managing and coordinating assigned treks.
3. *User (Trekker)*: A participant who books and participates in trekking activities.
4. Trek: A trekking event created and managed in the system

- Atrributes
  - Trek ID
  - Trek name
  - location
  - difficulty (of the trek) (Easy, moderate or hard)
  - Duration (in days)
  - Available Slots
  - Assigned staff id
  - status(pending / approved/ open/closed / closed)
  - payment status (optional)
  - extra fields etc.

5. Booking: A record of a user booking a trek

- Attributes
  - Booking ID
  - User ID
  - Trek ID
  - Booking Date
  - Status (Booked/ cancelled/ completed)
  - payment status (optional)
  - extra fields etc

6. Staff Profile: Details of a registered staff member.
- Attributes:

  - Staff ID
  - Name
  - Contact Details
  - Assigned Trek(s)
  - Status
  - Extra fields etc.

## Core Features - 

- *Authentication*
  - Login/register for Users (Trekker)
  - Login only for Admin and Trek Staff (no registration)
  - Only one Admin must exist and should be created programmatically
  - Role-based access control and authentication using Flask security (session or  token) or JWT based Token.
  - A unified user model to differentiate all types of user roles.

- *Admin Functionalities*
  - Admin dashboard showing:
    - Total number of treks
    - Total number of users and staffs 
    - total number of bookings 
  - Admin must pre-exist and be created programmatically after database creation. [No admin registration allowed]
  - Admin can:
    - Create and manage treks routes
    - Add a new trek staff
    - Assign staff to treks
    - View all bookings
    - Search users, staff, and treks
    - Deactivate or blacklist users/staff

- *Trek Staff Functionalities*
  - Staff dashboard should display:
    - Assigned treks by admin
    - Number of registered user per trek
  - Staff can:
    - Update trek slots and status
    - View and manage participant list
    - Mark trek as started/completed

- *User Functionalities*
  - Users must self-register and log in
  - User dashboard should display:
    - Available treks
    - Booked treks
    - Trek status
  - Users can:
    - Book treks
    - View booking status
    - View trekking history
    - Edit their profile
    - Search treks

## Backend Jobs (Using Celery)

1. Scheduled Job - Daily Reminders - 
The application should send daily reminders to users on g-chat using Google Chat Webhooks or SMS or mail.
  - Send reminders to users about upcoming treks, including trek start date, instructions etc.
  - Can be sent via email, SMS, or webhook 
  - Runs daily at a chosen time 

2. Scheduled Job - Monthly Activity Report - Devise a Monthly report for the admin created using HTML and sent via mail.

- Generate Monthly trekking activity report for Admin
- Includes:
  - number of treks conducted 
  - number of users participated 
  - popular treks 
- Generated on the first day of every month 
- Sent to Admin via email (HTML or PDF)

3. User Triggered Async Job - Export Booking History as CSV 
- Users can export their trekking history
- CSV should includes 
  - User ID
  - Trek Name
  - Location
  - Booking Status
  - Dates

- Triggered from user dashboard
- Export is triggered from the student dashboard.
- This should trigger a batch job, and send an alert once done.

## Performance and caching

- Use Redis caching for:
  - Frequently accessed treks

- Implement cache expiry
- Optimize API response times

## Other Core Functionalities

- Prevent overbooking beyond available slots
- Ensure only assigned staff can manage a trek
- Allow booking only when trek status is Open
- Prevent duplicate bookings for same trek
- Maintain complete trekking history per user
- Allow searching and filtering of treks
- Allow admin to view all historical trekking data

## Recommended and/or Optional Functionalities

- Well-designed PDF reports for Monthly activity reports (You can choose between HTML and PDF reports)
- Charts for analytics (popular treks, user participation) using ChartJS
- Single Responsive UI for both Mobile and Desktop
  - Unified UI that works across devices
  - Add to desktop feature

- Implementing frontend validation on all the form fields using HTML5 form validation or JavaScript
- Implementing backend validation within your APIs
- Provide styling and aesthetics to your application by creating responsive frontend using simple CSS or Bootstrap
- Notifications for booking confirmation/cancellation
- Basic payment simulation (optional)
- Any additional feature relevant to trekking systems

## the file structure 


backend/
│
├── app.py
├── models.py
├── config.py
├── requirements.txt
│
├── instance/
│   └── trekking.db
│
├── blueprints/
│   ├── auth.py
│   ├── admin.py
│   ├── staff.py
│   └── user.py
│
├── static/
├── templates/
└── ...