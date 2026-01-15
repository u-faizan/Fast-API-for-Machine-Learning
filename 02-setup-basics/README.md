# FastAPI for Machine Learning -  2: FastAPI Philosophy, Setup & First API

## What is FastAPI?

### Definition
**FastAPI** is a modern, high-performance web framework for building APIs with Python.

### Core Architecture
FastAPI is built on top of two Python libraries:

1. **Starlette** - Handles HTTP request/response processing
2. **Pydantic** - Provides data validation and type checking

---

## How FastAPI Works Internally

### Role of Starlette
- Receives incoming HTTP requests from clients
- Manages request processing
- Sends back HTTP responses to clients
- Handles the communication layer of the API

### Role of Pydantic
- **Data validation library** that checks if incoming data is in the correct format
- Provides type checking (Python lacks this by default)
- Validates data automatically before it reaches your API logic
- Ensures data integrity and correct data types

**Example use case**: If your API expects station names as strings and a date, Pydantic validates that the data is in the correct format and type before processing.

---

## Core Philosophy of FastAPI

FastAPI was created with **two primary philosophies**:

### 1. Fast to Run (High Performance)
APIs built with FastAPI execute quickly with:
- Very fast response times
- Ability to handle concurrent users
- Minimal latency
- High scalability

### 2. Fast to Code (Developer Efficiency)
The development process is streamlined:
- Minimal boilerplate code required
- Clean, simple syntax
- Quick API development
- Less code to achieve more functionality

---

## Understanding API Request Flow

### Components of a Deployed API

When you deploy an API (e.g., on AWS), two main components exist:

1. **API Code** - Contains your business logic (load model, make predictions, return response)
2. **Web Server** - Listens on machine ports for incoming HTTP requests

### Complete Request-Response Flow

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ (1) Sends HTTP Request
     │     (Feature values, POST method, URL, headers)
     ▼
┌──────────────┐
│ Web Server   │
└──────┬───────┘
       │ (2) Receives request
       │
       ▼
┌──────────────┐
│     SGI      │ (Server Gateway Interface)
│  (Translator)│ Converts HTTP → Python format
└──────┬───────┘
       │ (3) Python-readable format
       │
       ▼
┌──────────────┐
│  API Code    │
│  (Python)    │
│              │
│ predict()    │ (4) Processes request
│   ↓          │     Loads ML model
│ ML Model     │     Gets prediction
└──────┬───────┘
       │ (5) Python output
       │
       ▼
┌──────────────┐
│     SGI      │ Converts Python → HTTP format
└──────┬───────┘
       │ (6) HTTP Response (200 status, JSON)
       │
       ▼
┌──────────────┐
│ Web Server   │
└──────┬───────┘
       │ (7) Sends response
       ▼
┌──────────────┐
│   Client     │ Receives prediction
└──────────────┘
```

**Key Point**: SGI (Server Gateway Interface) acts as a translator between the web server and Python code, enabling two-way communication.

---

## Flask vs FastAPI: Performance Comparison

### Flask Architecture (Traditional Approach)

**Components**:
- **SGI Protocol**: WSGI (Web Server Gateway Interface)
- **WSGI Library**: Werkzeug
- **Web Server**: Gunicorn
- **Code Nature**: Synchronous

#### WSGI Characteristics
- **Synchronous nature** - Processes one request at a time
- **Blocking architecture** - When processing one request, others must wait
- Slower request processing
- Scalability challenges

**Example**: If 5 clients send requests simultaneously, WSGI processes them one by one in sequence.

```
Request 1 → Processing... (Request 2,3,4,5 wait)
Request 1 complete → Request 2 → Processing... (Request 3,4,5 wait)
```

#### Gunicorn Server
- WSGI HTTP server for Python applications
- Known for efficiency but has performance limitations
- Issues include IO wait times and high latency
- Struggles with highly scalable applications

---

### FastAPI Architecture (Modern Approach)

**Components**:
- **SGI Protocol**: ASGI (Asynchronous Server Gateway Interface)
- **ASGI Library**: Starlette
- **Web Server**: Uvicorn
- **Code Nature**: Asynchronous (supports async/await)

#### ASGI Characteristics
- **Asynchronous nature** - Handles multiple requests concurrently
- **Non-blocking architecture** - Doesn't wait for one request to finish
- Better suited for modern web applications
- Supports WebSockets and real-time features

**Example**: If 5 clients send requests, ASGI can process them simultaneously.

```
Request 1 → Processing
Request 2 → Processing  } All happening
Request 3 → Processing  } concurrently
Request 4 → Processing
Request 5 → Processing
```

#### Uvicorn Server
- High-performance ASGI server
- Asynchronous capabilities
- Handles concurrent requests efficiently
- Lower latency compared to Gunicorn

#### Async/Await in Python

FastAPI supports Python's `async` and `await` keywords for parallel processing.

**Without async** (Blocking):
```python
def predict():
    result = ml_model.predict(input)  # API waits here
    return result
# Cannot handle other requests while waiting
```

**With async** (Non-blocking):
```python
async def predict():
    result = await ml_model.predict(input)  # Can handle other requests
    return result
# While waiting for ML model, API serves other requests
```

---

### The Restaurant Analogy

#### Flask (Synchronous) - Single-Tasking Waiter
- Waiter takes order from Customer 1
- Goes to kitchen, places order
- **Stands and waits** until food is ready (blocking)
- Brings food to Customer 1
- Only then goes to Customer 2
- **Inefficient** - wastes time waiting

#### FastAPI (Asynchronous) - Multi-Tasking Waiter
- Waiter takes order from Customer 1
- Goes to kitchen, places order
- **Doesn't wait** - immediately goes to Customer 2 (non-blocking)
- Takes order from Customer 2, goes to kitchen
- Meanwhile, Customer 1's food is ready
- Brings Customer 1's food
- Continues serving multiple customers efficiently

---

## Why FastAPI is Fast to Code

### 1. Automatic Input Validation (via Pydantic)

FastAPI integrates Pydantic for automatic type checking and validation.

**Benefits**:
- Specify data types for function parameters
- Automatic validation happens behind the scenes
- No need to write manual validation code
- Prevents type-related errors

**Example** (will be shown in later videos):
```python
def get_trains(station1: str, station2: str, date: str):
    # Pydantic automatically validates types
    # No manual checking needed
```

### 2. Auto-Generated Interactive Documentation

FastAPI automatically creates documentation as you write code.

**Features**:
- Documentation generated at `/docs` endpoint
- **Interactive** - you can test APIs directly from the documentation
- Shows all endpoints, parameters, and response formats
- No need for separate documentation tools like Postman

**Access**: `http://your-api-url/docs`

### 3. Seamless Integration with Modern Libraries

FastAPI works seamlessly with popular libraries:

**Machine Learning/Deep Learning**:
- Scikit-learn
- TensorFlow
- PyTorch

**Authentication**:
- OAuth integration

**Database**:
- SQLAlchemy

**Deployment**:
- Docker
- Kubernetes

---

## Setting Up FastAPI

### Step 1: Create Project Folder
```bash
# Create a new folder for your project
mkdir api-tutorials
cd api-tutorials
```

### Step 2: Open in VS Code
```bash
code .
```

### Step 3: Create Virtual Environment
```bash
# Create virtual environment
python -m venv myenv

# Activate virtual environment (Windows)
myenv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source myenv/bin/activate
```

### Step 4: Install Required Libraries
```bash
pip install fastapi uvicorn pydantic
```

**Note**: Starlette is automatically installed with FastAPI.

---

## Building Your First API

### Step 1: Create Main File

Create a file named `main.py`:

```python
# Import FastAPI class
from fastapi import FastAPI

# Create FastAPI app object
app = FastAPI()

# Define endpoint with route decorator
@app.get("/")
def hello():
    return {"message": "Hello World"}
```

### Code Breakdown

1. **Import FastAPI**: `from fastapi import FastAPI`
2. **Create app object**: `app = FastAPI()`
3. **Define route**: `@app.get("/")` - This is the URL path
   - `@app.get` means this is a GET request
   - `"/"` means home route (root URL)
4. **Create function**: `hello()` - Executes when endpoint is hit
5. **Return response**: Returns a Python dictionary (converted to JSON automatically)

### Step 2: Run the API

```bash
uvicorn main:app --reload
```

**Command breakdown**:
- `uvicorn` - The ASGI server
- `main` - Your Python file name (without .py)
- `app` - Your FastAPI object name
- `--reload` - Auto-reload on code changes (development mode)

### Step 3: Access Your API

Open browser and go to:
```
http://127.0.0.1:8000/
```

**Output**:
```json
{
  "message": "Hello World"
}
```

---

## Adding Multiple Endpoints

### Create an "About" Endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return {
        "message": "Campus X is an education platform where you can learn AI"
    }
```

### Access Different Endpoints

**Home endpoint**:
```
http://127.0.0.1:8000/
```

**About endpoint**:
```
http://127.0.0.1:8000/about
```

---

## Interactive API Documentation

### Access Documentation

Navigate to:
```
http://127.0.0.1:8000/docs
```

### Features of Auto-Generated Docs

1. **Lists all endpoints** - Shows all routes in your API
2. **Shows request types** - GET, POST, etc.
3. **Interactive testing** - Try endpoints directly from browser
4. **No parameters needed** - Click "Try it out" → "Execute"
5. **Full HTTP response** - See status codes, headers, response body

### Testing an Endpoint from Docs

1. Click on an endpoint (e.g., GET `/`)
2. Click "Try it out"
3. Click "Execute"
4. View response:
   - Response body
   - Response headers
   - Status code (200)
   - Server information

**Benefit**: No need for Postman or other API testing tools!

---

## GET vs POST Requests

### GET Request
- Used to **fetch data** from the server
- Example: Retrieve train information

### POST Request
- Used to **send data** to the server
- Example: Submit user information

**Note**: POST requests will be covered in the next video.

---

## Key Takeaways

### FastAPI Performance Advantages
1. **Asynchronous** throughout the stack (ASGI, Uvicorn, async/await)
2. **Concurrent request handling** - Multiple requests processed simultaneously
3. **Lower latency** compared to Flask/WSGI-based frameworks
4. **Better scalability** for production applications

### FastAPI Development Advantages
1. **Automatic validation** via Pydantic
2. **Auto-generated interactive docs** at `/docs`
3. **Minimal boilerplate code**
4. **Seamless integration** with modern ML/AI libraries
5. **Fast development** with clean syntax

### Best Practices
- Use `--reload` flag during development for auto-updates
- Access `/docs` to test your API endpoints
- Structure your code with clear endpoint definitions
- Use type hints for automatic validation (covered in future videos)

---

## Next Steps
- Start a small project
- Learn core FastAPI features in depth
- Build more complex endpoints
- Implement POST requests
- Handle input parameters

---

## Comparison Summary Table

| **Feature** | **Flask (WSGI)** | **FastAPI (ASGI)** |
|------------|------------------|-------------------|
| **Protocol** | WSGI (Synchronous) | ASGI (Asynchronous) |
| **Server** | Gunicorn | Uvicorn |
| **Library** | Werkzeug | Starlette |
| **Processing** | One request at a time | Concurrent requests |
| **Architecture** | Blocking | Non-blocking |
| **Performance** | Slower, higher latency | Faster, lower latency |
| **Documentation** | Manual | Auto-generated |
| **Validation** | Manual | Automatic (Pydantic) |
| **Modern Features** | Limited | WebSockets, async/await |