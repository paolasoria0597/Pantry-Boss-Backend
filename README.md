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

# Simulate IoT: Simulating IoT Sensors for Dispenser Usage Tracking

This script, `simulate_iot.py`, is a **simulation tool** for testing a system that tracks dispenser usage in real time.
It mimics the behavior of **IoT sensors** that measure and report the consumption levels of dispensers (e.g., coffee
machines, snack dispensers, or beverage dispensers). The script allows us to test our backend system without needing
physical IoT hardware, making it an essential tool during development.

---

## **Real-World Application**

### **What Are IoT Sensors?**

IoT sensors are small, internet-enabled devices that monitor various physical conditions (like temperature, pressure, or
consumption levels) and send the data to a server. In this project, IoT sensors are imagined to be installed inside
dispensers to measure **current levels** of the dispenser's content (e.g., how much coffee is left).

### **How This Works in Real Life**

1. **Sensors Measure Usage**:
    - Each dispenser has an IoT sensor that tracks the remaining level of content (e.g., 75% full, 30% full).
    - The sensor sends this information to the backend server every few minutes.

2. **Backend Processes Data**:
    - The server receives the level data, updates the database, and checks if the dispenser is running low.

3. **Low-Level Alerts**:
    - If the dispenser level drops below a certain threshold (e.g., 20%), the system sends an **email notification** to
      the person responsible for refilling the dispenser.

4. **Why Automate This?**
    - In real-life scenarios, manual monitoring is inefficient, especially in environments like offices, airports, or
      shopping malls, where there are multiple dispensers.
    - IoT sensors automate this process, ensuring dispensers are refilled on time without relying on human checks.

---

## **Why Are We Simulating?**

1. **Hardware Is Expensive**:
    - IoT devices cost money and take time to set up. During development, it's easier and cheaper to simulate their
      behavior with software.

2. **Testing Without Physical Devices**:
    - This script pretends to be an IoT device, sending **fake data** (random consumption levels) to the server so we
      can test the system.

3. **Validating Alerts**:
    - The simulation ensures that low-level alerts (e.g., email notifications) work correctly when dispenser levels
      drop.

4. **Dynamic Behavior**:
    - IoT devices don’t send the same data every time. This script introduces randomness to simulate real-life usage
      patterns.

---

## **How `simulate_iot.py` Works**

The `simulate_iot.py` script is like a **virtual IoT sensor network**. It continuously updates the dispenser levels in
your Django server to simulate how real devices would work. Here's how it operates step by step:

---

### **1. Authenticate with the Server**

```python
def get_access_token(self):
    payload = {'username': USERNAME, 'password': PASSWORD}
    response = requests.post(AUTH_URL, json=payload)
```

- The script starts by **logging into the Django server** with a username and password.
- This generates a **JWT token**, which acts as proof that the script is authorized to send data to the server.

---

### **2. Fetch Dispenser IDs**

```python
def get_dispenser_ids(self, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(DISPENSER_URL, headers=headers)
```

- After logging in, the script retrieves a list of all dispenser IDs from the server.
- This ensures the script knows which dispensers exist and can update their levels.

---

### **3. Simulate Dispenser Usage**

```python
def simulate_dispenser_usage(self, dispenser_id, token):
    url = f"{DISPENSER_URL}{dispenser_id}/update-level/"
    payload = {'current_level': random.randint(1, 10)}
    response = requests.post(url, json=payload, headers=headers)
```

- The script **randomly selects a dispenser** and generates a random consumption value (e.g., "used 5 units").
- It sends this data to the server as if the dispenser itself reported the update.

---

### **4. Handle Expired Tokens**

```python
if not success:
    token = self.get_access_token()
```

- If the server responds with "unauthorized" (because the token expired), the script automatically re-authenticates by
  logging in again.
- This ensures the simulation runs continuously without interruptions.

---

### **5. Continuous Simulation**

```python
while True:
    dispenser_id = random.choice(dispenser_ids)
    self.simulate_dispenser_usage(dispenser_id, token)
    time.sleep(random.uniform(2, 5))
```

- The script runs in an **infinite loop**, continuously sending updates to simulate real-life, ongoing dispenser usage.
- A short delay (between 2 and 5 seconds) is added between updates to mimic the natural behavior of IoT sensors.

---

### **6. Graceful Exit**

```python
except KeyboardInterrupt:
self.stdout.write("Simulation interrupted. Exiting...")
```

- If the user manually stops the script (e.g., pressing `Ctrl+C`), it exits gracefully instead of crashing.

---

## **How to Use This Script**

### **1. Prerequisites**

- Make sure your Django server is running:
  ```bash
  python manage.py runserver
  ```

- Generate sample data so the script has dispensers to interact with:
  ```bash
  python manage.py generate_sample_data
  ```

### **2. Run the Script**

To start the simulation, run:

```bash
python manage.py simulate_iot
```

### **3. Stop the Simulation**

To stop the simulation, press:

```plaintext
Ctrl+C
```

---

## **Expected Behavior**

When you run the script:

1. It logs into the Django server using the provided credentials.
2. It retrieves a list of all dispensers.
3. It starts randomly simulating usage for each dispenser:
    - Picks a dispenser.
    - Decreases its current level by a random amount.
    - Sends the updated level to the server.

4. If the dispenser’s level gets too low, the Django server will:
    - Update the database.
    - Trigger an **email notification** to alert the user responsible for refilling the dispenser.

---

## **Real-World Benefits**

This simulation represents how IoT devices improve efficiency in environments with multiple dispensers:

1. **Automated Monitoring**:
    - No need for manual checks. The server automatically knows when a dispenser is running low.

2. **Timely Alerts**:
    - Users are notified before dispensers run out, avoiding situations where items (like coffee or snacks) are
      unavailable.

3. **Scalable System**:
    - Whether you have 10 dispensers or 1,000, the system works the same way, automatically updating and alerting as
      needed.

---
