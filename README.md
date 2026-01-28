# FastAPI for Machine Learning - Learning Journey 🚀

My comprehensive notes and code from the [CampusX FastAPI for ML YouTube Playlist](https://youtube.com/playlist?list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ&si=W2dUZjHamIQQhED5)

## 📚 Course Overview

This repository documents my learning journey through FastAPI, focusing on building production-ready APIs for Machine Learning models. The course is structured in three main parts:

1. **FastAPI Fundamentals** - Core concepts and basic project
2. **ML Integration** - Connecting FastAPI with ML models
3. **Deployment** - Docker, AWS, and production practices

---

## 🗂️ Repository Structure

```
Fast_API/
│
├── README.md                                    # This file - Main overview
├── .gitignore                                   # Git ignore rules
├── requirements.txt                             # All dependencies
│
├── 01-Introduction-to-APIs/
│   └── README.md                                # API concepts & architecture
│
├── 02-setup-basics/
│   ├── README.md                                # FastAPI philosophy & setup
│   └── basic_api.py                             # First Hello World API
│
├── 03-http-methods/
│   ├── README.md                                # HTTP methods & CRUD operations
│   ├── main.py                                  # Patient Management API (GET)
│   └── patients.json                            # Sample patient data
│
├── 04-path-query-params/
│   ├── README.md                                # Path & Query parameters guide
│   ├── main.py                                  # API with parameters
│   └── patients.json                            # Updated patient data
│
└── 05- optional - Pydantic Crash Course/
    ├── README.md                                # Complete Pydantic guide
    └── pydantic.ipynb                           # Jupyter notebook with examples
```

---

## 📖 Lecture Progress

### ✅ Lecture 1: Introduction to APIs
**Topics Covered:**
- What is an API and why we need it
- Monolithic vs API architecture
- Restaurant analogy for understanding APIs
- How APIs solve multi-platform problems
- APIs in Machine Learning context
- HTTP protocol and JSON format

**Key Takeaways:**
- APIs are connectors between software components
- Enable data sharing and multi-platform support
- Essential for ML model deployment
- Communication via HTTP, data exchange via JSON

📂 **Location:** [`01-Introduction-to-APIs/`](./01-Introduction-to-APIs/)

---

### ✅ Lecture 2: FastAPI Philosophy, Setup & First API
**Topics Covered:**
- FastAPI architecture (Starlette + Pydantic)
- ASGI vs WSGI comparison
- Async/await and non-blocking architecture
- Why FastAPI is fast (to run and to code)
- Virtual environment setup
- Building first "Hello World" API
- Auto-generated interactive documentation

**Key Takeaways:**
- FastAPI uses ASGI (asynchronous) vs Flask's WSGI (synchronous)
- Uvicorn server handles concurrent requests efficiently
- Automatic validation via Pydantic
- Interactive docs at `/docs` endpoint
- Minimal boilerplate code required

**Code Highlights:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World"}
```

📂 **Location:** [`02-setup-basics/`](./02-setup-basics/)

---

### ✅ Lecture 3: HTTP Methods & Project Setup
**Topics Covered:**
- Static vs Dynamic software
- CRUD operations (Create, Retrieve, Update, Delete)
- HTTP methods (GET, POST, PUT, DELETE)
- Patient Management System project introduction
- Loading data from JSON files
- Building first GET endpoint

**Key Takeaways:**
- All dynamic software interactions map to CRUD
- HTTP methods correspond to CRUD operations
- GET = Retrieve, POST = Create, PUT = Update, DELETE = Delete
- Helper functions for code reusability

**Project:** Patient Management System API
- View all patients endpoint (`/view`)
- JSON file as database
- Helper function for data loading

📂 **Location:** [`03-http-methods/`](./03-http-methods/)

---

### ✅ Lecture 4: Path & Query Parameters
**Topics Covered:**
- Path parameters for dynamic routes
- Query parameters for filtering/sorting
- Path() and Query() functions
- HTTPException for error handling
- HTTP status codes (200, 400, 404, etc.)
- Combining path and query parameters
- Type hints and automatic validation

**Key Takeaways:**
- Path params: `/patient/{id}` - identify specific resources
- Query params: `/sort?sort_by=height&order=desc` - filter/sort data
- FastAPI automatically validates parameter types
- Use HTTPException for proper error responses
- Can combine both for complex queries

**API Endpoints Built:**
- View specific patient by ID
- Sort patients by height/weight/BMI
- Filter and sort with validation

📂 **Location:** [`04-path-query-params/`](./04-path-query-params/)

---

### ✅ Optional: Pydantic Crash Course
**Topics Covered:**
- Why Pydantic is needed (type & data validation)
- Building Pydantic models with BaseModel
- Complex data types (List, Dict, Optional)
- Required vs Optional fields
- Custom data types (EmailStr, AnyUrl)
- Field() function for validation constraints
- Field validators for custom business logic
- Model validators for cross-field validation
- Computed fields
- Nested models
- Exporting models (model_dump, model_dump_json)

**Key Takeaways:**
- Pydantic solves type validation and data validation problems
- 3-step workflow: Build Model → Instantiate → Use
- Automatic type coercion when safe
- Field validators for single-field validation
- Model validators for multi-field validation
- Computed fields for calculated values
- Essential for FastAPI request/response validation

**Code Highlights:**
```python
from pydantic import BaseModel, Field, EmailStr

class Patient(BaseModel):
    name: str = Field(max_length=50)
    age: int = Field(gt=0, lt=120)
    email: EmailStr
```

📂 **Location:** [`05- optional - Pydantic Crash Course/`](./05-%20optional%20-%20Pydantic%20Crash%20Course/)

---

### ⏳ Upcoming Lectures
- Lecture 5: POST Requests & Creating Resources
- Lecture 6: PUT Requests & Updating Data
- Lecture 7: DELETE Requests
- Lecture 8: Error Handling & Validation
- Lecture 9: Docker Containerization
- Lecture 10: ML Model Integration
- Lecture 11: AWS Deployment

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/u-faizan/Fast-API-for-Machine-Learning.git
cd Fast_API
```

2. **Create virtual environment**
```bash
python -m venv myenv

# Windows
myenv\Scripts\activate

# Mac/Linux
source myenv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run any lecture's API**
```bash
# Example: Run Lecture 4 API
cd 04-path-query-params
uvicorn main:app --reload
```

5. **Access the API**
- API: http://127.0.0.1:8000
- Interactive Docs: http://127.0.0.1:8000/docs
- Alternative Docs: http://127.0.0.1:8000/redoc

---

## 📦 Dependencies

```txt
fastapi
uvicorn[standard]
pydantic
```

**Optional (for Pydantic Crash Course):**
```txt
jupyter
email-validator  # For EmailStr validation
```

---

## 🎯 Learning Objectives

By the end of this course, I will be able to:

- ✅ Understand API architecture and design principles
- ✅ Build RESTful APIs with FastAPI
- ✅ Implement CRUD operations
- ✅ Use path and query parameters effectively
- ✅ Validate data with Pydantic models
- ✅ Handle errors with proper HTTP status codes
- ⏳ Connect ML models to APIs
- ⏳ Deploy APIs to production (AWS)
- ⏳ Containerize applications with Docker

---

## 📝 Key Concepts Learned

### API Fundamentals
- API as a connector between software components
- Monolithic vs API-based architecture
- HTTP protocol and JSON data format
- RESTful API design principles

### FastAPI Specifics
- ASGI vs WSGI architecture
- Asynchronous request handling
- Automatic data validation with Pydantic
- Interactive API documentation
- Type hints and parameter validation
- HTTPException for error handling

### HTTP & CRUD
- GET, POST, PUT, DELETE methods
- CRUD operations mapping
- Path parameters for resource identification
- Query parameters for filtering/sorting
- HTTP status codes (200, 400, 404, 500)

### Pydantic
- Type validation and data validation
- BaseModel for creating schemas
- Field validators and model validators
- Computed fields for calculated values
- Nested models for complex structures
- Model serialization (dict/JSON)

---

## 🔗 Useful Resources

### Official Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

### Course Resources
- [YouTube Playlist](https://youtube.com/playlist?list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ&si=W2dUZjHamIQQhED5)
- [CampusX Website](https://learnwith.campusx.in/)

---

## 🛠️ Project: Patient Management System

A complete CRUD API for managing patient records, built progressively throughout the course.

**Features:**
- ✅ View all patients
- ✅ View patient by ID (with error handling)
- ✅ Sort patients by height/weight/BMI
- ✅ Validate data with Pydantic models
- ⏳ Create new patient (POST)
- ⏳ Update patient information (PUT)
- ⏳ Delete patient record (DELETE)

**Tech Stack:**
- FastAPI (Web framework)
- Uvicorn (ASGI server)
- Pydantic (Data validation)
- JSON (Data storage)

---

## 📊 Progress Tracker

| Lecture | Topic | Status | Notes | Code |
|---------|-------|--------|-------|------|
| 1 | Introduction to APIs | ✅ | [Link](./01-Introduction-to-APIs/) | - |
| 2 | FastAPI Setup & Basics | ✅ | [Link](./02-setup-basics/) | ✅ |
| 3 | HTTP Methods & CRUD | ✅ | [Link](./03-http-methods/) | ✅ |
| 4 | Path & Query Parameters | ✅ | [Link](./04-path-query-params/) | ✅ |
| - | Pydantic Crash Course (Optional) | ✅ | [Link](./05-%20optional%20-%20Pydantic%20Crash%20Course/) | ✅ |
| 5 | POST Requests | ⏳ | - | - |
| 6 | PUT Requests | ⏳ | - | - |
| 7 | DELETE Requests | ⏳ | - | - |
| 8 | Error Handling | ⏳ | - | - |
| 9 | Docker | ⏳ | - | - |
| 10 | ML Model Integration | ⏳ | - | - |
| 11 | AWS Deployment | ⏳ | - | - |

---

## 💡 Tips for Learning

1. **Follow Along**: Don't just read - code along with each lecture
2. **Experiment**: Try modifying the code to see what happens
3. **Use Docs**: Practice using the interactive `/docs` endpoint
4. **Read Errors**: FastAPI provides excellent error messages
5. **Test Everything**: Use the interactive docs to test your endpoints
6. **Review Pydantic**: Understanding Pydantic is crucial for FastAPI

---

## 🤝 Contributing

This is a personal learning repository, but feel free to:
- Report issues or errors in notes
- Suggest improvements
- Share additional resources
- Open pull requests for corrections

---

## 📧 Contact

**GitHub:** [@u-faizan](https://github.com/u-faizan)

---

## 📄 License

This project is for educational purposes. Course content belongs to CampusX.

---

## 🙏 Acknowledgments

- **CampusX** for the excellent FastAPI course
- **FastAPI** community for amazing documentation
- **Pydantic** team for powerful data validation
- All contributors to the FastAPI ecosystem

---

**Last Updated:** January 29, 2026

**Current Status:** Completed Lectures 1-4 + Pydantic Crash Course | Working on Lecture 5

---

## 🌟 Star This Repo

If you find these notes helpful, please consider giving this repository a star! ⭐
