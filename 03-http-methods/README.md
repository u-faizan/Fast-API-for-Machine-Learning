# FastAPI for Machine Learning -  3 : HTTP Methods & Project Setup

## Project Overview: Patient Management System

### Problem Statement

**Current Situation** (Offline System):
- Doctors provide paper prescriptions on clinic letterheads
- Patients must carry physical documents to every visit
- Documents stored in files over years
- Risk of documents being misplaced (both patient and doctor copies)
- Inefficient and unreliable system

**Solution** (Digital System):
Build a digital patient management system where doctors can:
- Maintain digital profiles for each patient
- Create, view, update, and delete patient records
- Store all data in one centralized location

### Patient Profile Structure

Each patient profile contains:
- Name
- City
- Age
- Gender
- Height
- Weight
- BMI (Body Mass Index)

**Note**: This is a basic-level project. In production, many more medical fields would be included.

### Project Scope

**What We're Building**: A backend API (not the front-end app)

**Storage**: JSON file (for simplicity)
- In production, you would use a proper database
- The same principles apply to both JSON files and databases

**API Endpoints** (5 total):

1. **Create** - Add new patient
2. **View All** - Retrieve all patients
3. **View One** - Retrieve specific patient by ID
4. **Update** - Modify existing patient record
5. **Delete** - Remove patient from database

---

## Understanding Software Classification

### Static vs Dynamic Software

#### Static Software
**Definition**: Software with minimal user interaction

**Characteristics**:
- Primarily for information retrieval
- One-way communication (software → user)
- Limited user actions

**Examples**:
- **Calendar** - View dates only, no interaction
- **Clock** - View time only, read-only access
- **Government websites** - Information display
- **Blogs** - Content consumption

#### Dynamic Software
**Definition**: Software with high user interaction

**Characteristics**:
- Two-way communication (user ↔ software)
- Multiple interaction possibilities
- User can manipulate data

**Examples**:
- **Microsoft Excel** - Create sheets, enter data, analyze, modify
- **Microsoft Word** - Create, edit, delete documents
- **Instagram** - Post, comment, like, scroll, edit
- **Zomato** - Order, view history, update address

---

## CRUD Operations

### The Four Types of Interactions

All dynamic software interactions fall into **four categories**, known as **CRUD**:

| **Letter** | **Operation** | **Description** |
|-----------|--------------|-----------------|
| **C** | Create | Add new data/resources |
| **R** | Retrieve (Read) | View/fetch existing data |
| **U** | Update | Modify existing data |
| **D** | Delete | Remove existing data |

### CRUD Examples in Different Software

#### Microsoft Excel
- **Create**: New worksheets, new cells with data
- **Retrieve**: View existing cells/data
- **Update**: Edit existing cell values
- **Delete**: Remove cells, sheets, data

#### Microsoft Word
- **Create**: New documents
- **Retrieve**: Open/read existing documents
- **Update**: Edit existing documents
- **Delete**: Remove documents

#### Instagram
- **Create**: Upload photos, write comments, create posts
- **Retrieve**: Scroll feed, view profiles
- **Update**: Edit profile, edit comments
- **Delete**: Delete posts, remove comments

#### Zomato
- **Create**: Place new order
- **Retrieve**: View past orders
- **Update**: Update delivery address
- **Delete**: Remove saved addresses

**Key Insight**: Every interaction with dynamic software maps to one of these four CRUD operations.

---

## Websites: Special Software

### What Makes Websites Different?

#### Regular Software (Desktop Applications)
- **Installation**: On the same machine being used
- **Execution**: Runs locally on user's machine
- Example: Microsoft Excel installed and used on your computer

#### Websites
- **Installation**: On a different machine (server)
- **Usage**: Accessed from another machine (client)
- **Communication**: Client ↔ Server via HTTP protocol

### Website Architecture

```
┌─────────────┐                    ┌─────────────┐
│   CLIENT    │ ←── HTTP ──→      │   SERVER    │
│  (Your PC)  │    Protocol        │ (Hosting)   │
└─────────────┘                    └─────────────┘
    Requests data                  Sends data back
```

### Static vs Dynamic Websites

#### Static Websites
- Minimal user interaction
- Mostly information display
- Examples: Blogs, government portals

#### Dynamic Websites
- High user interaction
- CRUD operations available
- Examples: Instagram, Zomato, Facebook

**Important**: Just like software, all website interactions can be categorized into CRUD operations.

---

## HTTP Methods

### Why HTTP Methods Matter

When clients communicate with servers via HTTP:
- Client sends **HTTP Request**
- Server sends back **HTTP Response**
- Request must specify **what type of interaction** is needed

### The Four Main HTTP Methods

HTTP methods (also called **HTTP verbs**) map directly to CRUD operations:

| **HTTP Method** | **CRUD Operation** | **Purpose** | **Example** |
|----------------|-------------------|-------------|-------------|
| **GET** | Retrieve (Read) | Fetch data from server | View profile page, scroll feed |
| **POST** | Create | Send data to server | Register, login, create post |
| **PUT** | Update | Modify existing resource | Edit profile, update comment |
| **DELETE** | Delete | Remove resource | Delete post, remove address |

### Method Details

#### GET Method
**Purpose**: Retrieve/view data from the server

**Characteristics**:
- Does NOT modify data
- Most commonly used method
- Safe and idempotent

**Examples**:
- Viewing a profile page
- Scrolling through Instagram feed
- Accessing courses page
- Reading blog posts

#### POST Method
**Purpose**: Send data to the server to create new resources

**Characteristics**:
- Sends data in request body
- Creates new resources
- NOT idempotent (multiple calls create multiple resources)

**Examples**:
- Filling login form
- Submitting registration form
- Creating new post
- Uploading photo

#### PUT Method
**Purpose**: Update existing resources on the server

**Characteristics**:
- Modifies existing data
- Replaces entire resource
- Idempotent (multiple identical calls have same effect)

**Examples**:
- Editing profile information
- Updating comment
- Changing address
- Modifying settings

#### DELETE Method
**Purpose**: Remove resources from the server

**Characteristics**:
- Deletes specified resource
- Idempotent
- Less commonly used than GET/POST

**Examples**:
- Deleting a post
- Removing a comment
- Deleting saved address
- Removing user account

---

## Live Demo: HTTP Methods in Action

### Viewing HTTP Requests in Browser

**Steps to inspect HTTP methods**:
1. Open browser Developer Tools (F12 or Right-click → Inspect)
2. Go to **Network** tab
3. Perform actions on website
4. Observe HTTP requests being sent

### Example 1: GET Request (Viewing Courses Page)

**Action**: Navigate to courses page

**What happens**:
- Browser sends GET request
- Request URL: `https://website.com/courses`
- Request Method: **GET**
- Server returns course page data

**CRUD Operation**: Retrieve

### Example 2: POST Request (Login)

**Action**: Fill login form and submit

**What happens**:
- Browser sends POST request
- Request URL: `https://website.com/authenticate`
- Request Method: **POST**
- Request contains email and password in body
- Server processes login

**CRUD Operation**: Create (creating a session)

---

## Project Setup

### Initial Setup

#### 1. Activate Virtual Environment
```bash
# Assuming you created myenv in previous video
myenv\Scripts\activate  # Windows
# or
source myenv/bin/activate  # Mac/Linux
```

#### 2. Create Data File

Create `patients.json` with sample data:

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "age": 35,
    "gender": "Male",
    "city": "New York",
    "height": 175,
    "weight": 70,
    "bmi": 22.9
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "age": 28,
    "gender": "Female",
    "city": "Los Angeles",
    "height": 165,
    "weight": 60,
    "bmi": 22.0
  },
  {
    "id": 3,
    "name": "Mike Johnson",
    "age": 42,
    "gender": "Male",
    "city": "Chicago",
    "height": 180,
    "weight": 85,
    "bmi": 26.2
  },
  {
    "id": 4,
    "name": "Sarah Williams",
    "age": 31,
    "gender": "Female",
    "city": "Houston",
    "height": 170,
    "weight": 65,
    "bmi": 22.5
  },
  {
    "id": 5,
    "name": "David Brown",
    "age": 45,
    "gender": "Male",
    "city": "Phoenix",
    "height": 178,
    "weight": 80,
    "bmi": 25.2
  }
]
```

---

## Building the API

### Step 1: Update Existing Endpoints

Modify `main.py` to reflect the project:

```python
from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {
        "message": "A fully functional API to manage your patients' records"
    }
```

### Step 2: Create Helper Function

**Purpose**: Load data from JSON file (reusable function)

```python
def load_data():
    """
    Helper function to load patient data from JSON file
    Returns: List of patient dictionaries
    """
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data
```

**Why create a helper function?**
- Code reusability - will be needed in multiple endpoints
- Cleaner code structure
- Easy to modify data source later (e.g., switch to database)

### Step 3: Create View All Patients Endpoint

```python
@app.get("/view")
def view():
    """
    Endpoint to retrieve all patient records
    HTTP Method: GET (because we're retrieving data)
    Returns: List of all patients
    """
    data = load_data()
    return data
```

### Complete Code (main.py)

```python
from fastapi import FastAPI
import json

app = FastAPI()

# Helper function to load data
def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

# Home endpoint
@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

# About endpoint
@app.get("/about")
def about():
    return {
        "message": "A fully functional API to manage your patients' records"
    }

# View all patients endpoint
@app.get("/view")
def view():
    data = load_data()
    return data
```

---

## Running and Testing the API

### Start the Server

```bash
uvicorn main:app --reload
```

**Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Test Endpoints

#### Test in Browser

**Home endpoint**:
```
http://127.0.0.1:8000/
```
**Response**:
```json
{
  "message": "Patient Management System API"
}
```

**About endpoint**:
```
http://127.0.0.1:8000/about
```
**Response**:
```json
{
  "message": "A fully functional API to manage your patients' records"
}
```

**View all patients endpoint**:
```
http://127.0.0.1:8000/view
```
**Response**: Returns all 5 patient records from JSON file

### Test in Interactive Docs

Navigate to:
```
http://127.0.0.1:8000/docs
```

**What you'll see**:
- Three GET endpoints listed
- Click on `/view` endpoint
- Click "Try it out"
- Click "Execute"
- View response with all patient data

---

## Understanding the Flow

### Request-Response Cycle for `/view` Endpoint

```
1. Client hits: http://127.0.0.1:8000/view
                ↓
2. FastAPI receives GET request
                ↓
3. Routes to view() function
                ↓
4. view() calls load_data()
                ↓
5. load_data() opens patients.json
                ↓
6. Reads JSON data
                ↓
7. Returns data to view()
                ↓
8. view() returns data to FastAPI
                ↓
9. FastAPI converts Python dict to JSON
                ↓
10. Sends JSON response to client
```

---

## Why Use GET Method for `/view`?

**Answer**: Because we're **retrieving** data (CRUD: Read operation)

**CRUD Mapping**:
- We're not creating anything → Not POST
- We're not updating anything → Not PUT
- We're not deleting anything → Not DELETE
- We're **reading/viewing** data → **GET** ✓

---

## Key Takeaways

### HTTP Methods Summary
1. **GET** - Retrieve/read data (most common)
2. **POST** - Create new resources
3. **PUT** - Update existing resources
4. **DELETE** - Remove resources

### CRUD Operations
- All dynamic software/websites support only **4 types of interactions**
- Every interaction maps to: Create, Retrieve, Update, or Delete
- HTTP methods correspond directly to CRUD operations

### Project Progress
- ✅ Project overview completed
- ✅ HTTP methods understood
- ✅ Helper function created (`load_data()`)
- ✅ First endpoint implemented (`/view`)
- ⏳ Remaining endpoints (view one, create, update, delete) - next videos

### Best Practices
- Create **helper functions** for reusable code
- Use appropriate **HTTP methods** based on operation type
- Use **descriptive endpoint names** (`/view`, not `/endpoint1`)
- Keep functions **simple and focused** (single responsibility)

---

## Next Steps

### Upcoming Features
1. **View specific patient** - Retrieve single patient by ID
2. **Filter/sort patients** - Sort by parameters (age, city, etc.)
3. **Query parameters** - Learn how to pass parameters in URLs

### Example
Instead of viewing all patients, view only:
- Patient with ID = 3
- Patients from a specific city
- Patients sorted by age

---

## Project Structure So Far

```
api-tutorials/
│
├── myenv/              # Virtual environment
├── main.py            # FastAPI application
└── patients.json      # Patient data (database)
```

---

## Common Errors and Solutions

### Error: "patients.json not found"
**Solution**: Ensure `patients.json` is in the same directory as `main.py`

### Error: "json module not found"
**Solution**: Import json at the top: `import json`

### Error: Server not reloading
**Solution**: Make sure you used `--reload` flag when starting uvicorn

### Response shows file path instead of data
**Solution**: Make sure you're returning `data`, not `f` (the file object)