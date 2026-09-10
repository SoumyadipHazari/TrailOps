# Database Information about the Project


The database contains 3 tables `User` , `Trek`, `Booking` 

> as this application follows a unified user model meaning *Admin* , *Trek Staff* and *User* itself are all stored in a single `User` table and later differentiated using the role attribute.

1. User Table as `users`

| Column         | Data Type   | Description                     |
| -------------- | ----------- | ------------------------------- |
| id             | Integer     | Primary Key                     |
| name           | String(200) | Full Name                       |
| email          | String(200) | User Email (Unique)             |
| password_hash  | String(255) | Encrypted Password              |
| phone          | String(50)  | Contact Number                  |
| role           | String(30)  | admin / staff / user            |
| status         | String(30)  | active / inactive / blacklisted |
| experience     | Integer     | Staff experience (nullable)     |
| specialization | String(150) | Staff specialization (nullable) |

Stores information about all users of the application which includes --

- Admin
- Trek Staff
- Trek Users

2. Trek Table as `treks`

Stores all trekking events and their details

| Column          | Data Type   | Description               |
| --------------- | ----------- | ------------------------- |
| id              | Integer     | Primary Key               |
| name            | String(200) | Trek Name                 |
| location        | String(200) | Trek Location             |
| description     | Text        | Trek Description          |
| difficulty      | String(30)  | Easy / Moderate / Hard    |
| duration        | Integer     | Duration in Days          |
| start_date      | Date        | Trek Start Date           |
| end_date        | Date        | Trek End Date             |
| available_slots | Integer     | Number of Available Seats |
| staff_id        | Integer     | Assigned Trek Staff       |
| status          | String(40)  | Trek Status               |

3. Booking Table as `bookings`

Stores every trek booking made by users and its following details.

| Column         | Data Type  | Description             |
| -------------- | ---------- | ----------------------- |
| id             | Integer    | Primary Key             |
| user_id        | Integer    | User making booking     |
| trek_id        | Integer    | Trek booked             |
| booking_date   | DateTime   | Date of Booking         |
| status         | String(30) | Booking Status          |
| payment_status | String(30) | Optional Payment Status |


