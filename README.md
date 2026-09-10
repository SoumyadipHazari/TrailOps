# TrailOps - Trekking Management Application 

*TrailOps* is a role-based trekking management web application built using **Flask**.
It supports **Admin, Trek Staff and User** workflows including creating treks, booking a trek and managing the staffs and users or customers.

---

## Project Information

- **Name:** TrailOps
- **Developer:** Soumyadip Hazari
- **Course:** Modern Application Development II 

---


## Features Overview

### Authentication & Roles 
- Secure login & registration 
- Role-based access control:
  - **Admin**
  - **Trek Staff**
  - **User**

---

### Admin Features
- Add and manage trekking routes
- Can add and manage trek staffs
- Can assign staff to treks
- Can view and manage all users, staff and treks
- Can search users, staff or treks 
- Can deactivate or blacklist users or staff
- Can view reports and trekking statistics.

---

### Trek Staff
- Can view assigned treks by admin 
- Can manage trek details such as:
  - Available slots 
  - Trek Status (open/closed)
- Can view list of registered users for their treks 
- Can Update trek completion Status

### User (Trekker)
-Can view approved/open treks
- can search and filter treks based on difficulty, location, and duration
- Can book treks
- Can view booking status and trekking history
- Edit Profile details

---


## Database Design

Database contains three tables `User`, `Trek` and `Booking`.
As per the problem statement A unified User model is used from there we will gonna differentiate roles i.e; `Admin`, `User` and `Trek Staff.

```
                 USER
------------------------------------------------

id (PK)

name

email (Unique)

password_hash

phone

role

status

experience

specialization

created_at



                     1
                     |
                     |
                     |
                     N


                 TREK
------------------------------------------------

id (PK)

name

location

description

difficulty

duration

start_date

end_date

available_slots

staff_id (FK)

status

created_at



                     1
                     |
                     |
                     |
                     N


              BOOKING
------------------------------------------------

id (PK)

user_id (FK)

trek_id (FK)

booking_date

status

payment_status

--------------------------------------------------
where the flow will be like this

User

↓

Trek

↓

Booking

↑

User
```

1. User table as `users`

| Column | Data Type | Description |
|--------|-----------|-------------|
| id | Integer | Primary Key |
| name | String(200) | Full Name |
| email | String(200) | User Email (Unique) |
| password_hash | String(255) | Encrypted Password |
| phone | String(50) | Contact Number |
| role | String(30) | admin / staff / user |
| status | String(30) | active / inactive / blacklisted |
| experience | Integer | Staff experience (nullable) |

Stores information about all the users of the application which includes --

- Admin
- Trek Staff
- Trek Users

2. Trek Table as `treks`

stores all trekking events and their details

| Column | Data Type | Description |
|--------|-----------|-------------|
| id | Integer | Primary Key |
| name | String(200) | Trek Name |
| location | String(200) | Trek Location |
| description | Text | Trek Description |
| difficulty | String(30) | Easy / Moderate / Hard |
| duration | Integer | Duration in Days |
| start_date | Date | Trek Start Date |
| end_date | Date | Trek End Date |
| available_slots | Integer | Number of Available Seats |
| staff_id | Integer | Assigned Trek Staff |
| status | String(40) | Trek Status |

Booking table as `bookings`

Stores every trek booking made by users and its following details 

| Column | Data Type | Description |
|--------|-----------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | User making booking |
| trek_id | Integer | Trek booked |
| booking_date | DateTime | Date of Booking |
| status | String(30) | Booking Status |

---

# To run the application 

- Creating .venv in root folder

`python3 -m venv .venv`

- Activating the .venv

`source .venv/bin/activate`

- Installing the packages 

`pip install -r requirements.txt`

- Running the backend

`python app.py`

- Starting the Redis (new terminal)
`redis-server`

- Installing the frontend (new terminal)

`cd /frontend`

`npm install`

- Running the frontend 
`npm run dev`

- Running the backend jobs (new terminal)

`celery -A celery_config.celery worker --loglevel=info`

