# School Management System

**School Management System** is a Django-based web application that simplifies the management of students, teachers, staff, and school-related operations. It helps administrators and staff manage various aspects of school activities, such as student records, teacher assignments, staff management, and library transactions.

## Features

- **Student Management**: Add, edit, and manage student details such as attendance, grades, and classes.
- **Teacher Management**: Manage teacher profiles, subject assignments, and schedules.
- **Staff Management**: Track administrative staff, including roles, schedules, and payroll.
- **Library Management**: Keep track of books, library transactions, and student borrowing history.
- **Role-Based Access Control (RBAC)**: Different roles with specific permissions (Admin, Teacher, Staff, and Student).
- **Session Management**: Secure user sessions to ensure privacy and data integrity.
- **User Authentication**: Login and logout functionality with role-based redirection.

## Tech Stack

- **Backend**: Django 4.x
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Authentication**: Django’s built-in user authentication system

## Installation

### Prerequisites

- Python 3.x
- Django 4.x

### Steps to Set Up

1. Clone the repository:

2. Install dependencies:

3. Set up your database:

4. Create a superuser for the admin interface:

5. Start the development server:

6. Access the application at `http://127.0.0.1:8000/

# Role-Based Access Control (RBAC) System

## Permissions and Role-Based Access
The application utilizes Role-Based Access Control (RBAC) to manage different user roles and their associated permissions. The primary roles in the system are:

- **Admin**: Has full access to all aspects of the system, including managing students, office staff, librarians, library transactions, fees records, and more.
- **Office Staff**: Can view all student details, manage fees history, and view library borrowing records for students.
- **Librarian**: Can view student details and library borrowing history but does not have permission to edit or manage records.
- **Student**: Can view their personal profile, attendance records, grades, and fees history.

### Role Permissions

#### Admin:
- Full access to all models and views (students, office staff, librarians, library, fees records, etc.).
- Can create, update, and delete records for all users and resources.
- Can assign roles to users.
- Manages CRUD operations for student, library, and fees records.

#### Office Staff:
- Can view all student details.
- Can manage the fees history (add, edit, delete records).
- Can view the library history for students.

#### Librarian:
- Can view student details and library borrowing history (view-only access).
- Cannot edit or delete records related to library transactions.

#### Student:
- Can view their personal information, attendance records, grades, and fees history.
- Cannot edit any records other than their own profile.

## Session Management
The system uses Django’s built-in session management for secure login and user authentication. Sessions are handled as follows:

- **Login**: When a user logs in, a session is created, storing their user ID and role in the session data.
- **Session Expiration**: Sessions expire after a set time or if the user manually logs out. Users will be logged out after a period of inactivity.
- **Session Security**: Django provides built-in protection against session hijacking and session fixation attacks.

Django’s session framework ensures that each user interacts with the application based on their permissions and role while maintaining security.

## Features and Views

### Authentication
- Implement login functionality using Django's authentication framework.
- Restrict access to views and actions based on user roles using Django's permissions system.

### Admin Dashboard
- Manage (create, edit, delete) office staff and librarian accounts.
- Perform CRUD operations on student, library, and fees records.

### Office Staff Dashboard
- View all student details.
- Manage fees history.
- View library history for students.

### Librarian Dashboard
- View-only access to student details and library history.

### Student Management
- Create, update, view, and delete student details.

### Library History
- View and manage (add, edit, delete) library borrowing records for students.

### Fees History
- View and manage (add, edit, delete) fees records for students.

## Usage
- **Admin Dashboard**: Log in as an admin to manage office staff, librarians, students, and library records.
- **Office Staff Access**: Office staff can view student details, manage fees, and view library history.
- **Librarian Access**: Librarians can view student and library records.
- **Student Access**: Students can view their own personal information, attendance, grades, and fees history.

## Contributing
We welcome contributions! If you'd like to contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-xyz`).
3. Commit your changes (`git commit -m 'Add feature xyz'`).
4. Push to the branch (`git push origin feature-xyz`).
5. Open a pull request to merge your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- **Django** - Web framework used.
- **SQLite** - Database used.
