# FastAPI for Machine Learning -  4 : Path & Query Parameters

## Overview
This section covers two crucial concepts in FastAPI:
1. **Path Parameters** - Dynamic segments in URLs to identify specific resources
2. **Query Parameters** - Optional parameters for filtering, sorting, and searching

---

## Path Parameters

### Definition
**Path Parameters** are dynamic segments of a URL path used to identify a specific resource.

### Understanding with Example

#### Scenario: View All Patients (Previous Section)
```
URL: http://localhost:8000/view
Result: Shows data of ALL patients
```

#### New Requirement: View Specific Patient
```
URL: http://localhost:8000/view/3
Result: Shows data of ONLY patient with ID = 3
```

### URL Structure with Path Parameters

```
http://localhost:8000/patient/3
         ↑              ↑       ↑
      Domain       Endpoint   Path Parameter
                            (Dynamic Part)
```

**Key Points**:
- **Static parts**: `localhost:8000/patient` (cannot be changed)
- **Dynamic part**: `3` (can be changed by different clients)
- Client A might request: `/patient/3`
- Client B might request: `/patient/4`
- Client C might request: `/patient/5`

### Purpose of Path Parameters

Path parameters help **locate a specific resource** among many resources on the server.

**Use Cases**:
1. **Retrieve** - View specific user profile, specific product
2. **Update** - Modify a particular patient record
3. **Delete** - Remove a specific resource

---

## Implementing Path Parameters

### Step 1: Define Route with Path Parameter

```python
from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    """Helper function to load patient data"""
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str):
    """
    Endpoint to view a specific patient
    patient_id: Dynamic path parameter
    """
    # Load all patient data
    data = load_data()
    
    # Check if patient exists
    if patient_id in data:
        return data[patient_id]
    else:
        return {"error": "Patient not found"}
```

### Code Breakdown

**Route Definition**: `@app.get("/patient/{patient_id}")`
- `/patient/` - Static part of URL
- `{patient_id}` - Dynamic variable (path parameter)
- Curly braces `{}` indicate a path parameter

**Function Parameter**: `patient_id: str`
- Variable name must match the route parameter
- Type annotation specifies expected data type
- In our case: `str` because IDs are like "P001", "P002"

**Logic**:
1. Load all patient data using `load_data()`
2. Check if `patient_id` exists in data dictionary
3. If exists: return patient data
4. If not: return error message

### Updated patients.json Structure

```json
{
  "P001": {
    "name": "John Doe",
    "age": 35,
    "gender": "Male",
    "city": "New York",
    "height": 175,
    "weight": 70,
    "bmi": 22.9
  },
  "P002": {
    "name": "Jane Smith",
    "age": 28,
    "gender": "Female",
    "city": "Los Angeles",
    "height": 165,
    "weight": 60,
    "bmi": 22.0
  },
  "P003": {
    "name": "Mike Johnson",
    "age": 42,
    "gender": "Male",
    "city": "Chicago",
    "height": 180,
    "weight": 85,
    "bmi": 26.2
  }
}
```

### Testing the Endpoint

**Browser testing**:
```
http://localhost:8000/patient/P001  → Returns John Doe's data
http://localhost:8000/patient/P003  → Returns Mike Johnson's data
http://localhost:8000/patient/P005  → Returns error
```

**Interactive Docs testing**:
```
http://localhost:8000/docs
→ Navigate to /patient/{patient_id}
→ Click "Try it out"
→ Enter P001 in patient_id field
→ Click "Execute"
→ View response
```

---

## Enhancing Path Parameters with `Path()` Function

### Why Use Path()?

The `Path()` function enhances path parameters by:
1. **Adding descriptions** - Explain what the parameter expects
2. **Providing examples** - Show sample values
3. **Adding validation** - Enforce constraints (min, max, regex)
4. **Improving documentation** - Makes API more user-friendly

### Path() Function Capabilities

```python
from fastapi import Path

Path(
    ...,                          # Required (three dots)
    title="Patient ID",           # Title for documentation
    description="ID of patient",  # Detailed description
    example="P001",               # Example value
    min_length=4,                 # Minimum length validation
    max_length=10,                # Maximum length validation
    regex="^P[0-9]{3}$",         # Pattern validation
    gt=0,                         # Greater than (for integers)
    ge=0,                         # Greater than or equal
    lt=100,                       # Less than
    le=100                        # Less than or equal
)
```

### Implementation

```python
from fastapi import FastAPI, Path

@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,  # Three dots = required parameter
        description="ID of the patient in the database",
        example="P001"
    )
):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    else:
        return {"error": "Patient not found"}
```

### Benefits in Documentation

After adding `Path()`, the auto-generated docs show:
- **Description**: "ID of the patient in the database"
- **Example**: "P001"
- Clear indication that it's a **required** parameter

This helps clients understand exactly what format to use.

---

## HTTP Status Codes

### What Are Status Codes?

**HTTP Status Codes** are 3-digit numbers returned by a server to indicate the result of a client's request.

### Status Code Categories

| **Range** | **Category** | **Meaning** |
|-----------|-------------|-------------|
| **2xx** | Success | Request was successful |
| **3xx** | Redirection | Further action needed |
| **4xx** | Client Error | Problem with client request |
| **5xx** | Server Error | Problem on server side |

### Common Status Codes

#### 2xx - Success Codes

| **Code** | **Name** | **Meaning** |
|----------|----------|-------------|
| **200** | OK | Request successful, data returned |
| **201** | Created | Resource successfully created |
| **204** | No Content | Success, but no data to return (used in DELETE) |

#### 4xx - Client Error Codes

| **Code** | **Name** | **Meaning** |
|----------|----------|-------------|
| **400** | Bad Request | Missing fields, wrong data type |
| **401** | Unauthorized | Login required to access resource |
| **403** | Forbidden | Logged in but not allowed to access |
| **404** | Not Found | Resource doesn't exist |

#### 5xx - Server Error Codes

| **Code** | **Name** | **Meaning** |
|----------|----------|-------------|
| **500** | Internal Server Error | Something went wrong on server |
| **502** | Bad Gateway | HTTP communication broken |
| **503** | Service Unavailable | Server down or overloaded |

---

## Problem: Incorrect Status Code

### The Issue

Current code returns **200 (Success)** even when patient is not found:

```python
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    else:
        return {"error": "Patient not found"}  # ❌ Returns 200 status
```

**Problem**: 
- Patient "P007" doesn't exist
- Response: `{"error": "Patient not found"}`
- Status Code: **200** (Success) ❌
- Should be: **404** (Not Found) ✓

### Solution: HTTPException

**HTTPException** is a special built-in exception in FastAPI used to return custom HTTP error responses with appropriate status codes.

### Using HTTPException

```python
from fastapi import FastAPI, Path, HTTPException

@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the database",
        example="P001"
    )
):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    else:
        # Raise HTTPException with 404 status code
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
```

### Testing with HTTPException

**Request**: `http://localhost:8000/patient/P007`

**Response**:
```json
{
  "detail": "Patient not found"
}
```

**Status Code**: **404** ✓

---

## Complete Code with Improvements

```python
from fastapi import FastAPI, Path, HTTPException
import json

app = FastAPI()

# Helper function
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

# View all patients
@app.get("/view")
def view():
    data = load_data()
    return data

# View specific patient with path parameter
@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the database",
        example="P001"
    )
):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
```

---

## Query Parameters

### Definition
**Query Parameters** are optional values appended to the end of a URL to pass additional data for operations like filtering, sorting, searching, and pagination.

### URL Structure with Query Parameters

```
http://localhost:8000/sort?sort_by=height&order=descending
                      ↑    ↑                ↑
                  Endpoint  ?          Query Parameters
                        (Question mark separates endpoint from parameters)
```

**Syntax**:
- `?` - Separates endpoint from query parameters
- `key=value` - Query parameter format
- `&` - Separates multiple query parameters

### Characteristics

| **Feature** | **Path Parameters** | **Query Parameters** |
|-------------|-------------------|---------------------|
| **Location** | Part of URL path | After `?` in URL |
| **Required** | Yes (usually) | No (optional) |
| **Purpose** | Identify specific resource | Filter, sort, search |
| **Example** | `/patient/P001` | `/sort?sort_by=age` |

---

## Use Case: Sorting Patients

### Requirements

Create an endpoint that allows clients to:
1. **Sort** patient data by different columns (height, weight, BMI)
2. **Order** results in ascending or descending order
3. Make both parameters **optional** (use defaults if not provided)

### Implementation

#### Step 1: Define Endpoint with Query Parameters

```python
from fastapi import FastAPI, Query, HTTPException

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,  # Required parameter
        description="Sort on the basis of height, weight, and BMI"
    ),
    order: str = Query(
        "ascending",  # Default value (makes it optional)
        description="Sort in ascending or descending order"
    )
):
    # Implementation here
    pass
```

#### Step 2: Add Validation

```python
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight, and BMI"),
    order: str = Query("ascending", description="Sort in ascending or descending order")
):
    # Define valid options
    valid_fields = ["height", "weight", "bmi"]
    
    # Validate sort_by
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_fields}"
        )
    
    # Validate order
    if order not in ["ascending", "descending"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Select between ascending and descending"
        )
    
    # Continue with sorting logic
```

#### Step 3: Implement Sorting Logic

```python
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight, and BMI"),
    order: str = Query("ascending", description="Sort in ascending or descending order")
):
    # Validation
    valid_fields = ["height", "weight", "bmi"]
    
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_fields}"
        )
    
    if order not in ["ascending", "descending"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Select between ascending and descending"
        )
    
    # Load data
    data = load_data()
    
    # Determine sort order (reverse=True for descending)
    sort_order = True if order == "descending" else False
    
    # Sort data
    sorted_data = sorted(
        data.values(),
        key=lambda x: x[sort_by],
        reverse=sort_order
    )
    
    return sorted_data
```

---

## Understanding the Sorting Code

### Lambda Function Explanation

```python
sorted_data = sorted(
    data.values(),           # Get all patient dictionaries
    key=lambda x: x[sort_by], # Sort by this field
    reverse=sort_order        # True = descending, False = ascending
)
```

**Breakdown**:
- `data.values()` - Extract all patient dictionaries from main dictionary
- `key=lambda x: x[sort_by]` - For each patient `x`, use value of `sort_by` column as sort key
- `reverse=sort_order` - If `True`, sorts in descending order; if `False`, ascending

### Example Walkthrough

**Request**: `http://localhost:8000/sort?sort_by=height&order=descending`

**Process**:
1. `sort_by = "height"`
2. `order = "descending"`
3. Validation passes ✓
4. `sort_order = True` (because order is "descending")
5. Sort all patients by their `height` value
6. `reverse=True` → Highest height first
7. Return sorted list

**Result**:
```json
[
  {"name": "Mike", "height": 180, ...},  // Tallest
  {"name": "John", "height": 175, ...},
  {"name": "Sarah", "height": 170, ...},
  {"name": "Jane", "height": 165, ...}   // Shortest
]
```

---

## Query() Function Details

### Purpose
The `Query()` function in FastAPI is used to declare, validate, and document query parameters.

### Features

```python
from fastapi import Query

Query(
    default_value,              # Default if not provided
    title="Parameter Title",    # Title in docs
    description="Details",      # Description
    example="sample_value",     # Example value
    min_length=1,              # Minimum string length
    max_length=50,             # Maximum string length
    regex="^[a-z]+$",          # Pattern validation
    gt=0,                      # Greater than (numbers)
    ge=0,                      # Greater or equal
    lt=100,                    # Less than
    le=100                     # Less or equal
)
```

### Default Values

**Required parameter** (no default):
```python
sort_by: str = Query(...)  # Three dots = required
```

**Optional parameter** (with default):
```python
order: str = Query("ascending")  # Default = "ascending"
```

**Optional parameter** (None as default):
```python
filter: str = Query(None)  # Default = None (truly optional)
```

---

## Testing Query Parameters

### Browser Testing

**Test 1: Both parameters**
```
http://localhost:8000/sort?sort_by=height&order=descending
```
Result: Patients sorted by height, tallest first

**Test 2: Only required parameter**
```
http://localhost:8000/sort?sort_by=bmi
```
Result: Patients sorted by BMI in ascending order (default)

**Test 3: Invalid sort_by**
```
http://localhost:8000/sort?sort_by=age&order=ascending
```
Result: 400 error - "Invalid field. Select from ['height', 'weight', 'bmi']"

**Test 4: Invalid order**
```
http://localhost:8000/sort?sort_by=weight&order=random
```
Result: 400 error - "Invalid order. Select between ascending and descending"

### Interactive Docs Testing

Navigate to: `http://localhost:8000/docs`

**Steps**:
1. Find `/sort` endpoint
2. Click "Try it out"
3. See two input fields:
   - `sort_by` (required)
   - `order` (optional, default: "ascending")
4. Enter values:
   - sort_by: "bmi"
   - order: "descending"
5. Click "Execute"
6. View response with sorted data

---

## Complete Sorting Endpoint Code

```python
from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,
        description="Sort on the basis of height, weight, and BMI"
    ),
    order: str = Query(
        "ascending",
        description="Sort in ascending or descending order"
    )
):
    """
    Sort patients by specified field and order
    
    Args:
        sort_by: Column to sort by (height, weight, bmi)
        order: Sort order (ascending or descending)
    
    Returns:
        Sorted list of patients
    """
    # Define valid options
    valid_fields = ["height", "weight", "bmi"]
    
    # Validate sort_by parameter
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_fields}"
        )
    
    # Validate order parameter
    if order not in ["ascending", "descending"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Select between ascending and descending"
        )
    
    # Load patient data
    data = load_data()
    
    # Determine sort order
    sort_order = True if order == "descending" else False
    
    # Sort data by specified field
    sorted_data = sorted(
        data.values(),
        key=lambda x: x[sort_by],
        reverse=sort_order
    )
    
    return sorted_data
```

---

## Path vs Query Parameters Comparison

| **Aspect** | **Path Parameters** | **Query Parameters** |
|-----------|-------------------|---------------------|
| **Syntax** | `/patient/{id}` | `/sort?sort_by=age` |
| **Required** | Yes (usually) | No (optional) |
| **Purpose** | Identify specific resource | Filter/sort/search data |
| **Position** | Part of URL path | After `?` in URL |
| **Use Case** | GET/UPDATE/DELETE one item | Filter, sort, paginate |
| **Example** | View patient P001 | Sort by age, page 2 |
| **Function** | `Path()` | `Query()` |

---

## Combining Path and Query Parameters

You can use **both** in a single endpoint:

```python
@app.get("/patient/{patient_id}/records")
def get_patient_records(
    patient_id: str = Path(..., description="Patient ID"),
    year: int = Query(2024, description="Filter by year"),
    limit: int = Query(10, description="Number of records to return")
):
    """
    Get patient records with filtering
    
    URL: /patient/P001/records?year=2023&limit=5
    """
    # Implementation
    pass
```

**Example URLs**:
```
/patient/P001/records?year=2023&limit=5
/patient/P002/records?year=2024
/patient/P003/records
```

---

## Key Takeaways

### Path Parameters
- ✅ Identify **specific resources**
- ✅ **Required** by default
- ✅ Part of URL path structure
- ✅ Use for: GET one, UPDATE, DELETE operations
- ✅ Enhanced with `Path()` function

### Query Parameters
- ✅ **Optional** parameters for filtering/sorting
- ✅ Added after `?` in URL
- ✅ Use for: Search, filter, sort, paginate
- ✅ Can have **default values**
- ✅ Enhanced with `Query()` function

### HTTP Status Codes
- ✅ Use **200** for successful requests
- ✅ Use **400** for client errors (bad input)
- ✅ Use **404** for resource not found
- ✅ Always use `HTTPException` for proper error responses

### Best Practices
1. **Always validate** path and query parameters
2. **Use appropriate status codes** with HTTPException
3. **Provide descriptions and examples** for better documentation
4. **Set sensible defaults** for optional query parameters
5. **Return meaningful error messages** when validation fails

---

## Next Steps

In upcoming videos, we'll cover:
- **POST requests** - Create new patient records
- **PUT requests** - Update existing patient data
- **DELETE requests** - Remove patient records
- **Request body** handling
- **Pydantic models** for complex data validation

---

## Project Structure Update

```
api-tutorials/
│
├── myenv/              # Virtual environment
├── main.py            # FastAPI application
└── patients.json      # Patient data (dictionary format now)
```

**Updated patients.json** (dictionary with IDs as keys):
```json
{
  "P001": {...},
  "P002": {...},
  "P003": {...}
}
```