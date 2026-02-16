# Microservices Architecture with API Gateway (FastAPI)

A modern, scalable microservices project demonstrating the **API Gateway Pattern** using Python, FastAPI, and JWT authentication. The system is designed to handle student and course management through a centralized entry point.

# 🚀 Modular API Gateway & Microservices (FastAPI)

This project demonstrates a scalable **Microservices Architecture** using an **API Gateway** pattern. It features centralized authentication, domain-specific modular routing, and cross-cutting concerns like logging and error handling.

---

## 🏗️ Project Structure
```text
microservices-fastapi/
├── gateway/                 # API Gateway Service (Port 8000)
│   ├── main.py              # Entry point & Router registration
│   ├── config.py            # Global settings & Service URLs
│   ├── auth.py              # JWT Auth logic
│   ├── utils/
│   │   └── forwarder.py     # Core request forwarding logic
│   └── routes/
│       ├── auth.py          # /login endpoint
│       ├── students.py      # /gateway/students routes
│       └── courses.py       # /gateway/courses routes
├── student-service/         # Student Microservice (Port 8001)
│   ├── main.py              # FastAPI app & endpoints
│   ├── models.py            # Pydantic data schemas
│   ├── service.py           # Business logic layer
│   └── data_service.py      # Mock data repository
├── course-service/          # Course Microservice (Port 8002)
│   ├── main.py              # FastAPI app & endpoints
│   ├── models.py            # Pydantic data schemas
│   ├── service.py           # Business logic layer
│   └── data_service.py      # Mock data repository
├── requirements.txt         # Project dependencies
└── venv/                    # Python virtual environment
```

This project consists of three independent services working together:

* **API Gateway (Port 8000):** The single entry point. Handles authentication, request routing, and logging.
* **Student Microservice (Port 8001):** Manages student records and profiles
* **Course Microservice (Port 8002):** Manages academic course data
  

## 🛠️ Tech Stack

* **Language:** Python 3.8+
* **Framework:** FastAPI
* **ASGI Server:** Uvicorn
* **Authentication:** JWT (JSON Web Tokens) 
* **Asynchronous Client:** HTTPx (for service-to-service communication) 
  
## 📥 Getting Started

### 1. Prerequisites
Ensure you have Python installed on your system.

### 2. Installation
Clone the repository and set up a virtual environment:

```bash
# Create and activate virtual environment
python -m venv venv 
source venv/bin/activate  

# On Windows use: 
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Services
To run the full architecture, you must start each service in a separate terminal:

```bash
# Terminal 1 (Student Service):
cd student-service
uvicorn main:app --reload --port 8001
```

```bash
# Terminal 2 (Course Service):
cd course-service
uvicorn main:app --reload --port 8002
```

```bash
# Terminal 3 (API Gateway):
cd gateway
uvicorn main:app --reload --port 8000
```

### 4. 🔐 Authentication

All gateway routes (except `/login`) are secured using **JSON Web Tokens (JWT)**.

### Login

Send a `POST` request to:

http://localhost:8000/login

### 5. Default Credentials

```json
{
  "username": "admin",
  "password": "password123"
}
```

### Using the Token

Include the returned JWT token in the header for all protected requests:

Authorization: Bearer <token>

---

### 6. 📍 API Endpoints (Gateway)

### 🎓 Student Service

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/gateway/students` | Retrieve all students |
| GET | `/gateway/students/{id}` | Retrieve a specific student by ID |
| POST | `/gateway/students` | Create a new student record |
| PUT | `/gateway/students/{id}` | Update existing student details |
| DELETE | `/gateway/students/{id}` | Remove a student record from the system |

---

### 📚 Course Service

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/gateway/courses` | Retrieve all courses |
| GET | `/gateway/courses/{id}` | Retrieve a specific course by ID |
| POST | `/gateway/courses` | Create a new course record |
| PUT | `/gateway/courses/{id}` | Update existing course details |
| DELETE | `/gateway/courses/{id}` | Remove a course record from the system |

---

### 7. 🧪 Testing

The project includes built-in interactive documentation via **Swagger UI** for easy endpoint testing.

### 🔗 Documentation URLs

- Gateway API Docs: http://localhost:8000/docs
- Direct Student API Docs: http://localhost:8001/docs
- Direct Course API Docs: http://localhost:8002/docs

---

## 🛡️ Key Features

## Modular Routing
Utilizes FastAPI `APIRouter` to decouple domain logic into clean, manageable files.

## Centralized Logging
Middleware intercepts all gateway traffic to log:
- Request paths
- Status codes
- Execution time

## Robust Error Handling
Custom exception handlers ensure the Gateway returns structured JSON responses even if a microservice is offline  
(`503 Service Unavailable`).

## Separation of Concerns
Each microservice manages its own data and business logic independently.