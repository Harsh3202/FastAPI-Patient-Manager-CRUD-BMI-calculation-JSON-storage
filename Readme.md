# 🏥 FastAPI Patient Manager

A simple **Patient Management System** built with **FastAPI** that supports **CRUD operations**, **BMI calculation**, and stores patient data in a JSON file.

## 📌 Features
- Create, Read, Update, and Delete patient records
- Calculate **BMI** based on height & weight
- Store patient data persistently in JSON format
- RESTful API endpoints
- FastAPI interactive docs with Swagger UI

## 🚀 Tech Stack
- **Python 3.9+**
- **FastAPI**
- **Uvicorn**
- **JSON** for storage

## 📂 Project Structure
```
FastApi/
│-- main.py         # Main FastAPI application
│-- patients.json   # JSON file storing patient data
│-- requirements.txt
└-- README.md
```

## ⚡ Installation & Usage
1. **Clone the repository**
```bash
git clone https://github.com/Harsh3202/FastAPI-Patient-Manager-CRUD-BMI-calculation-JSON-storage.git
cd FastAPI-Patient-Manager-CRUD-BMI-calculation-JSON-storage
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
uvicorn main:app --reload
```

4. **Access API docs**
```
Swagger UI: http://127.0.0.1:8000/docs
ReDoc:      http://127.0.0.1:8000/redoc
```

## 📬 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/patients` | Get all patients |
| GET    | `/patients/{id}` | Get patient by ID |
| POST   | `/patients` | Add a new patient |
| PUT    | `/patients/{id}` | Update patient info |
| DELETE | `/patients/{id}` | Delete a patient |

## 📝 License
This project is licensed under the MIT License.
