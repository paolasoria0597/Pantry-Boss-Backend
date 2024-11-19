Here's a detailed `README.md` for your project:

---

# Dispenser Management API

## Overview

The **Dispenser Management API** is a Django-based backend system for managing floors, pantries, and dispensers. It
supports user authentication, CRUD operations for floors, pantries, and dispensers, and custom functionality for
updating dispenser levels with automated low-level notifications.

## Features

- **Authentication**
    - User registration and login with JWT tokens.
    - Token refresh functionality.
- **Floor Management**
    - Create, update, delete, and filter floors by associated users.
- **Pantry Management**
    - Create, update, delete, and filter pantries by associated floors.
- **Dispenser Management**
    - Create, update, delete, and filter dispensers by associated pantries.
    - Update dispenser levels and send notifications when running low.
- **Documentation**
    - API is documented with Swagger using `drf-yasg`.

---

## Technologies Used

- **Backend Framework:** Django Rest Framework (DRF)
- **Authentication:** JWT (via `rest_framework_simplejwt`)
- **Email Notifications:** Django `send_mail`
- **API Documentation:** Swagger (`drf-yasg`)

---

## Installation

### Prerequisites

1. Python 3.8+
2. Django 4.x+
3. PostgreSQL or SQLite (default Django database)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Authentication

| Endpoint                | Method | Description              |
|-------------------------|--------|--------------------------|
| `/users/register/`      | POST   | Register a new user      |
| `/users/login/`         | POST   | Login and get JWT tokens |
| `/users/token/refresh/` | GET    | Refresh JWT tokens       |

### Floor Management

| Endpoint        | Method | Description                            |
|-----------------|--------|----------------------------------------|
| `/floors/`      | GET    | List all floors (filterable by `user`) |
|                 | POST   | Create a new floor                     |
| `/floors/<id>/` | GET    | Retrieve a specific floor by ID        |
|                 | PUT    | Update a specific floor by ID          |
|                 | DELETE | Delete a specific floor by ID          |

### Pantry Management

| Endpoint          | Method | Description                               |
|-------------------|--------|-------------------------------------------|
| `/pantries/`      | GET    | List all pantries (filterable by `floor`) |
|                   | POST   | Create a new pantry                       |
| `/pantries/<id>/` | GET    | Retrieve a specific pantry by ID          |
|                   | PUT    | Update a specific pantry by ID            |
|                   | DELETE | Delete a specific pantry by ID            |

### Dispenser Management

| Endpoint                         | Method | Description                                  |
|----------------------------------|--------|----------------------------------------------|
| `/dispensers/`                   | GET    | List all dispensers (filterable by `pantry`) |
|                                  | POST   | Create a new dispenser                       |
| `/dispensers/<id>/`              | GET    | Retrieve a specific dispenser by ID          |
|                                  | PUT    | Update a specific dispenser by ID            |
|                                  | DELETE | Delete a specific dispenser by ID            |
| `/dispensers/<id>/update-level/` | POST   | Update dispenser level and notify if low     |

---

## Filtering Examples

- **List floors for a specific user:**
  ```
  GET /floors/?user_id=1
  ```
- **List pantries for a specific floor:**
  ```
  GET /pantries/?floor=2
  ```
- **List dispensers for a specific pantry:**
  ```
  GET /dispensers/?pantry=3
  ```

---

## Notifications

When a dispenser's level falls below its threshold, an email notification is sent to the specified recipient. The email
includes details about the dispenser's location and type.

---

## Swagger Documentation

Visit `/swagger/` in your browser (after starting the server) to view the auto-generated API documentation. You can
interact with the API directly from the Swagger interface.

---
