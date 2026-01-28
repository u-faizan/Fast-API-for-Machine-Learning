---

# Pydantic Crash Course - Data Validation in Python

## Overview

**Pydantic** is a Python library for data validation and settings management. It's essential for production-grade code, especially when building APIs, working with configuration files, or creating ML pipelines.

**Why Learn Pydantic?**

- Used extensively in FastAPI
- Required for production-level code
- Common in data science ML pipelines
- Industry-standard for data validation

---

## The Two Big Problems Pydantic Solves

### Problem 1: Type Validation

### The Challenge in Python

Python is a **dynamically typed language** with no built-in static typing:

```python
# Python allows this (problematic in production)
x = 10        # x is integer
x = "hello"   # Now x is string - no error!
```

### Real-World Problem Example

**Scenario**: Senior programmer creates a function to insert patient data into database.

```python
# Senior programmer's code
def insert_patient_data(name, age):
    # Imagine database insertion code here
    print(f"Inserting into database...")
    print(f"Name: {name}")
    print(f"Age: {age}")

# Junior programmer uses the function
insert_patient_data("Nitish", "30")  # Bug! Age is string, not int
```

**Problem**: Code runs successfully but inserts wrong data type into database! ❌

### Attempted Solution 1: Type Hinting

```python
def insert_patient_data(name: str, age: int):
    print(f"Inserting into database...")
    print(f"Name: {name}")
    print(f"Age: {age}")

# This still works even with wrong type!
insert_patient_data("Nitish", "30")  # No error - type hints don't enforce
```

**Limitation**: Type hints are **informational only** - they don't produce errors or enforce types.

### Attempted Solution 2: Manual Type Checking

```python
def insert_patient_data(name: str, age: int):
    # Manual type validation
    if type(name) == str and type(age) == int:
        print(f"Inserting into database...")
        print(f"Name: {name}")
        print(f"Age: {age}")
    else:
        raise TypeError("Incorrect data type")

# Now this raises an error ✓
insert_patient_data("Nitish", "30")  # TypeError!
```

**Problem with Manual Validation**:

- ❌ Not scalable
- ❌ Boilerplate code repeated everywhere
- ❌ Hard to maintain as fields increase

**Example of Scaling Problem**:

```python
# Function 1: Insert
def insert_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
        # Insert logic
        pass
    else:
        raise TypeError("Incorrect data type")

# Function 2: Update (same validation code!)
def update_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:  # Duplicated!
        # Update logic
        pass
    else:
        raise TypeError("Incorrect data type")

# Adding a new field (weight) requires updating ALL functions!
```

---

### Problem 2: Data Validation

Beyond type checking, you need **business logic validation**:

```python
def insert_patient_data(name: str, age: int):
    # Type validation
    if type(name) == str and type(age) == int:
        # Data validation - age can't be negative
        if age < 0:
            raise ValueError("Age cannot be negative")
        else:
            # Insert logic
            print(f"Inserting {name}, age {age}")
    else:
        raise TypeError("Incorrect data type")
```

**More Validation Requirements**:

- Email must be valid format
- Phone number must follow pattern
- Age must be in range (0-120)
- Name max length 50 characters
- And many more...

**Result**: Massive boilerplate code that needs to be repeated across all functions! ❌

---

## How Pydantic Solves These Problems

### The Three-Step Pydantic Workflow

```
Step 1: Build Model (Define Schema)
         ↓
Step 2: Instantiate with Raw Data (Automatic Validation)
         ↓
Step 3: Use Validated Object in Functions
```

### Step 1: Build Pydantic Model

**Define the ideal schema** using a Pydantic class:

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
```

**What this does**:

- Defines required fields
- Specifies data types
- Sets validation rules (more on this later)

### Step 2: Instantiate Model with Raw Data

**Create object from raw data** - validation happens automatically:

```python
# Raw input data (could come from API, form, file, etc.)
patient_data = {
    "name": "Nitish",
    "age": 30
}

# Create Pydantic object (validation happens here!)
patient1 = Patient(**patient_data)
```

**What happens during instantiation**:

- ✅ Checks if all required fields are present
- ✅ Validates data types
- ✅ Applies any validation rules
- ✅ Converts types automatically when possible
- ❌ Raises ValidationError if anything fails

### Step 3: Use Validated Object

**Pass validated object to your function**:

```python
def insert_patient_data(patient: Patient):
    # Now we're guaranteed correct data!
    print(f"Inserting into database...")
    print(f"Name: {patient.name}")
    print(f"Age: {patient.age}")

# Use the validated object
insert_patient_data(patient1)
```

---

## Complete Example: Before vs After Pydantic

### Before Pydantic (Manual Validation)

```python
def insert_patient_data(name: str, age: int):
    # Manual type validation
    if type(name) == str and type(age) == int:
        # Manual data validation
        if age < 0:
            raise ValueError("Age cannot be negative")
        else:
            print(f"Inserting {name}, age {age}")
    else:
        raise TypeError("Incorrect data type")

def update_patient_data(name: str, age: int):
    # Same validation code repeated!
    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("Age cannot be negative")
        else:
            print(f"Updating {name}, age {age}")
    else:
        raise TypeError("Incorrect data type")

# Using the functions
insert_patient_data("Nitish", 30)      # Works
insert_patient_data("Nitish", "30")    # TypeError
insert_patient_data("Nitish", -5)      # ValueError
```

### After Pydantic (Clean & Scalable)

```python
from pydantic import BaseModel, Field

# Step 1: Define schema ONCE
class Patient(BaseModel):
    name: str
    age: int = Field(gt=0)  # Greater than 0

# Step 2: Functions use the model
def insert_patient_data(patient: Patient):
    print(f"Inserting {patient.name}, age {patient.age}")

def update_patient_data(patient: Patient):
    print(f"Updating {patient.name}, age {patient.age}")

# Step 3: Create validated objects
patient_data = {"name": "Nitish", "age": 30}
patient1 = Patient(**patient_data)

# Use in functions
insert_patient_data(patient1)  # Works ✓
update_patient_data(patient1)  # Works ✓

# This will fail validation automatically
bad_data = {"name": "Nitish", "age": "30"}
patient2 = Patient(**bad_data)  # Auto-converts "30" to 30!

# This will raise ValidationError
invalid_data = {"name": "Nitish", "age": -5}
patient3 = Patient(**invalid_data)  # ValidationError: age must be > 0
```

**Benefits**:

- ✅ Validation logic defined once in model
- ✅ No repeated boilerplate code
- ✅ Easy to add new fields (update model only)
- ✅ Automatic type conversion when safe
- ✅ Clear error messages

---

## Installation

### Install Pydantic V2

```bash
pip install pydantic
```

**Important**: Always use **Pydantic V2** (not V1)

**Why V2?**

- Written in Rust (much faster)
- More features and improvements
- Industry standard
- Better performance for production code

**Check version**:

```python
import pydantic
print(pydantic.__version__)  # Should be 2.x.x
```

---

## Building Complex Pydantic Models

### Basic Data Types

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str           # String
    age: int            # Integer
    weight: float       # Float
    height: float       # Float
    bmi: float         # Float
    is_married: bool   # Boolean
```

### Complex Data Types: Lists and Dictionaries

**Problem**: Can't use built-in `list` and `dict` directly for type validation.

```python
# ❌ Wrong - only validates it's a list, not contents
class Patient(BaseModel):
    allergies: list  # Only checks if it's a list
```

**Solution**: Import from `typing` module for nested type validation:

```python
from typing import List, Dict
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    bmi: float
    is_married: bool
    allergies: List[str]              # List of strings
    contact_details: Dict[str, str]   # Dictionary with string keys & values
```

**Why use `List[str]` instead of `list`?**

- `list` only validates that it's a list
- `List[str]` validates:
    - ✅ It's a list
    - ✅ Every item inside is a string

**Example**:

```python
from typing import List, Dict
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    is_married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

# Create patient object
patient_data = {
    "name": "Nitish",
    "age": 30,
    "weight": 75.2,
    "is_married": True,  # or 1 (auto-converts)
    "allergies": ["Pollen", "Dust"],
    "contact_details": {
        "email": "abc@gmail.com",
        "phone": "1234567890"
    }
}

patient = Patient(**patient_data)
print(patient.name)      # Nitish
print(patient.allergies) # ['Pollen', 'Dust']
```

**Validation in Action**:

```python
# ❌ This will fail - integer in allergies list
bad_data = {
    "name": "John",
    "age": 25,
    "weight": 70.0,
    "is_married": False,
    "allergies": ["Pollen", 123],  # Integer not allowed!
    "contact_details": {"email": "test@test.com", "phone": "999"}
}

patient = Patient(**bad_data)  # ValidationError!

# ❌ This will fail - integer value in dictionary
bad_data2 = {
    "name": "John",
    "age": 25,
    "weight": 70.0,
    "is_married": False,
    "allergies": ["Pollen"],
    "contact_details": {
        "email": "test@test.com",
        "phone": 1234567890  # Integer not allowed!
    }
}

patient2 = Patient(**bad_data2)  # ValidationError!
```

---

## Required vs Optional Fields

### Required Fields (Default Behavior)

**All fields are required by default** in Pydantic models:

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
    weight: float

# ❌ This fails - missing 'weight'
patient_data = {"name": "John", "age": 30}
patient = Patient(**patient_data)  # ValidationError: field required
```

### Making Fields Optional

**Use `Optional` from typing module**:

```python
from typing import Optional, List
from pydantic import BaseModel

class Patient(BaseModel):
    name: str              # Required
    age: int               # Required
    weight: float          # Required
    is_married: bool       # Required
    allergies: Optional[List[str]] = None  # Optional with default None
```

**Syntax Breakdown**:

- `Optional[Type]` - Marks field as optional
- `= None` - Sets default value (required for optional fields)

**Example**:

```python
from typing import Optional, List
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
    allergies: Optional[List[str]] = None
    is_married: Optional[bool] = False  # Default is False

# Without allergies (uses default None)
patient1 = Patient(name="John", age=30)
print(patient1.allergies)    # None
print(patient1.is_married)   # False

# With allergies
patient2 = Patient(name="Jane", age=25, allergies=["Dust"])
print(patient2.allergies)    # ['Dust']
```

### Setting Default Values

You can set defaults for any field (not just optional ones):

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
    is_married: bool = False  # Default value
    country: str = "USA"      # Default value

# Without specifying defaults
patient = Patient(name="John", age=30)
print(patient.is_married)  # False
print(patient.country)     # USA

# Overriding defaults
patient2 = Patient(name="Jane", age=25, is_married=True, country="UK")
print(patient2.is_married)  # True
print(patient2.country)     # UK
```

---

## Data Validation Methods

### Method 1: Custom Data Types from Pydantic

Pydantic provides **built-in data types** for common validation scenarios:

### EmailStr - Email Validation

```python
from pydantic import BaseModel, EmailStr

class Patient(BaseModel):
    name: str
    email: EmailStr  # Validates email format

# Valid email
patient1 = Patient(name="John", email="john@gmail.com")  # ✓

# Invalid email
patient2 = Patient(name="Jane", email="notanemail")  # ValidationError
patient3 = Patient(name="Bob", email="bob@invalid")  # ValidationError
```

**What EmailStr validates**:

- Contains `@` symbol
- Valid email format
- Proper domain structure

### AnyUrl - URL Validation

```python
from pydantic import BaseModel, AnyUrl

class Patient(BaseModel):
    name: str
    linkedin_url: AnyUrl  # Validates URL format

# Valid URLs
patient1 = Patient(
    name="John",
    linkedin_url="https://linkedin.com/in/john"
)  # ✓

patient2 = Patient(
    name="Jane",
    linkedin_url="http://example.com"
)  # ✓

# Invalid URLs
patient3 = Patient(
    name="Bob",
    linkedin_url="linkedin.com"  # Missing http://
)  # ValidationError

patient4 = Patient(
    name="Alice",
    linkedin_url="not a url"
)  # ValidationError
```

**What AnyUrl validates**:

- Proper URL protocol (`http://`, `https://`, `file://`, etc.)
- Valid URL structure
- Can be web URL or file URL

### Other Built-in Types

```python
from pydantic import (
    BaseModel,
    EmailStr,
    AnyUrl,
    HttpUrl,      # Only HTTP/HTTPS URLs
    FilePath,     # Valid file path
    DirectoryPath, # Valid directory path
    IPvAnyAddress, # IP address validation
    PositiveInt,  # Integer > 0
    NegativeInt,  # Integer < 0
    constr,       # Constrained string
    conint        # Constrained integer
)

class AdvancedPatient(BaseModel):
    email: EmailStr
    website: HttpUrl
    profile_pic: FilePath
    age: PositiveInt
```

---

### Method 2: Field Function for Custom Validation

The `Field()` function allows **custom validation rules** based on your business logic:

```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    name: str
    age: int
    weight: float
```

### Numeric Constraints

**Greater Than (gt)**:

```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    weight: float = Field(gt=0)  # Weight must be > 0

patient1 = Patient(weight=70.5)   # ✓
patient2 = Patient(weight=-10)    # ValidationError: must be > 0
patient3 = Patient(weight=0)      # ValidationError: must be > 0
```

**Greater Than or Equal (ge)**:

```python
class Patient(BaseModel):
    age: int = Field(ge=0)  # Age must be >= 0

patient = Patient(age=0)   # ✓
patient = Patient(age=-1)  # ValidationError
```

**Less Than (lt)**:

```python
class Patient(BaseModel):
    age: int = Field(lt=150)  # Age must be < 150

patient = Patient(age=120)  # ✓
patient = Patient(age=150)  # ValidationError
```

**Less Than or Equal (le)**:

```python
class Patient(BaseModel):
    temperature: float = Field(le=106.0)  # Temp <= 106°F

patient = Patient(temperature=98.6)   # ✓
patient = Patient(temperature=110.0)  # ValidationError
```

**Range Validation (Combining gt/lt or ge/le)**:

```python
class Patient(BaseModel):
    age: int = Field(gt=0, lt=120)  # 0 < age < 120
    bmi: float = Field(ge=10.0, le=50.0)  # 10 <= BMI <= 50

patient1 = Patient(age=30, bmi=22.5)  # ✓
patient2 = Patient(age=0, bmi=22.5)   # ValidationError: age must be > 0
patient3 = Patient(age=150, bmi=22.5) # ValidationError: age must be < 120
patient4 = Patient(age=30, bmi=5.0)   # ValidationError: BMI must be >= 10
```

### String Constraints

**Max Length**:

```python
class Patient(BaseModel):
    name: str = Field(max_length=50)  # Max 50 characters

patient1 = Patient(name="John Doe")  # ✓
patient2 = Patient(name="A" * 100)   # ValidationError: max 50 chars
```

**Min Length**:

```python
class Patient(BaseModel):
    name: str = Field(min_length=2)  # At least 2 characters

patient1 = Patient(name="Jo")  # ✓
patient2 = Patient(name="J")   # ValidationError: min 2 chars
```

**Exact Length**:

```python
class Patient(BaseModel):
    zip_code: str = Field(min_length=5, max_length=5)  # Exactly 5 chars

patient1 = Patient(zip_code="12345")  # ✓
patient2 = Patient(zip_code="1234")   # ValidationError
patient3 = Patient(zip_code="123456") # ValidationError
```

### List Constraints

**Max Items**:

```python
from typing import List
from pydantic import BaseModel, Field

class Patient(BaseModel):
    allergies: List[str] = Field(max_length=5)  # Max 5 allergies

patient1 = Patient(allergies=["Pollen", "Dust"])  # ✓
patient2 = Patient(allergies=["A", "B", "C", "D", "E", "F"])  # ValidationError
```

**Min Items**:

```python
class Patient(BaseModel):
    medications: List[str] = Field(min_length=1)  # At least 1 medication

patient1 = Patient(medications=["Aspirin"])  # ✓
patient2 = Patient(medications=[])  # ValidationError: need at least 1
```

### Complete Example with Multiple Constraints

```python
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, EmailStr

class Patient(BaseModel):
    # String with max length
    name: str = Field(max_length=50)

    # Integer with range
    age: int = Field(gt=0, lt=120)

    # Float with range
    weight: float = Field(gt=0, description="Weight in kg")
    height: float = Field(gt=0, le=300, description="Height in cm")
    bmi: float = Field(ge=10.0, le=50.0)

    # Email validation
    email: EmailStr

    # List with max items
    allergies: Optional[List[str]] = Field(default=None, max_length=10)

    # Optional with default
    is_married: bool = False

# Valid patient
patient_data = {
    "name": "John Doe",
    "age": 30,
    "weight": 75.5,
    "height": 175.0,
    "bmi": 24.7,
    "email": "john@example.com",
    "allergies": ["Pollen", "Dust"]
}

patient = Patient(**patient_data)  # ✓

# Invalid examples
patient_data["age"] = -5          # ValidationError: age must be > 0
patient_data["weight"] = 0        # ValidationError: weight must be > 0
patient_data["bmi"] = 60          # ValidationError: BMI must be <= 50
patient_data["email"] = "invalid" # ValidationError: invalid email
patient_data["allergies"] = ["A"] * 15  # ValidationError: max 10 items
```

---

## Field() Function: Adding Metadata

Beyond validation, `Field()` is used to **add descriptions and documentation**:

```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    name: str = Field(
        max_length=50,
        description="Full name of the patient"
    )

    age: int = Field(
        gt=0,
        lt=120,
        description="Patient's age in years",
        example=30
    )

    email: EmailStr = Field(
        description="Patient's email address",
        example="patient@example.com"
    )
```

**Where metadata is useful**:

- **API Documentation**: Appears in FastAPI's auto-generated docs
- **Code Readability**: Helps other developers understand fields
- **IDE Support**: Better autocomplete and hints

**Example in FastAPI docs**:
When you build an API with FastAPI, this metadata appears in the `/docs` page, helping clients understand what each field expects.

---

## Automatic Type Conversion

Pydantic automatically converts types **when safe to do so**:

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int

# String "30" automatically converted to int 30
patient_data = {"name": "John", "age": "30"}
patient = Patient(**patient_data)

print(patient.age)        # 30 (int, not string!)
print(type(patient.age))  # <class 'int'>
```

**Safe Conversions**:

```python
# String to int (if valid number)
Patient(age="30")      # ✓ → 30

# String to bool
Patient(is_married="true")   # ✓ → True
Patient(is_married="1")      # ✓ → True
Patient(is_married="false")  # ✓ → False
Patient(is_married="0")      # ✓ → False

# Int to bool
Patient(is_married=1)   # ✓ → True
Patient(is_married=0)   # ✓ → False

# Float to int (truncates)
Patient(age=30.9)  # ✓ → 30
```

**Unsafe Conversions (Will Fail)**:

```python
# Can't convert invalid string to int
Patient(age="thirty")  # ✗ ValidationError

# Can't convert random string to bool
Patient(is_married="maybe")  # ✗ ValidationError
```

---

## Complete Working Example

```python
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, EmailStr, AnyUrl

class Patient(BaseModel):
    # Basic fields with validation
    name: str = Field(
        max_length=50,
        description="Patient's full name"
    )

    age: int = Field(
        gt=0,
        lt=120,
        description="Patient's age in years"
    )

    weight: float = Field(
        gt=0,
        description="Weight in kilograms"
    )

    height: float = Field(
        gt=0,
        le=300,
        description="Height in centimeters"
    )

    bmi: float = Field(
        ge=10.0,
        le=50.0,
        description="Body Mass Index"
    )

    # Built-in validators
    email: EmailStr = Field(description="Patient's email")
    linkedin_url: Optional[AnyUrl] = None

    # Optional fields
    is_married: Optional[bool] = False
    allergies: Optional[List[str]] = Field(
        default=None,
        max_length=5,
        description="List of allergies"
    )

    # Complex types
    contact_details: Dict[str, str] = Field(
        description="Contact information"
    )

# Function using the model
def insert_patient_data(patient: Patient):
    print(f"Inserting patient: {patient.name}")
    print(f"Age: {patient.age}")
    print(f"Email: {patient.email}")
    print(f"Allergies: {patient.allergies}")

# Valid data
patient_data = {
    "name": "John Doe",
    "age": 30,
    "weight": 75.5,
    "height": 175.0,
    "bmi": 24.7,
    "email": "john@example.com",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "is_married": True,
    "allergies": ["Pollen", "Dust"],
    "contact_details": {
        "phone": "1234567890",
        "address": "123 Main St"
    }
}

# Create validated patient object
patient = Patient(**patient_data)

# Use in function
insert_patient_data(patient)

# Access fields
print(patient.name)       # John Doe
print(patient.age)        # 30
print(patient.allergies)  # ['Pollen', 'Dust']
```

---

## Key Takeaways

### Why Use Pydantic?

1. **✅ Type Validation** - Enforces correct data types
2. **✅ Data Validation** - Enforces business rules (ranges, formats, etc.)
3. **✅ No Boilerplate** - Write validation rules once in model
4. **✅ Automatic Conversion** - Safe type conversions happen automatically
5. **✅ Clear Errors** - Helpful error messages when validation fails
6. **✅ Self-Documenting** - Models serve as documentation
7. **✅ IDE Support** - Better autocomplete and type hints

### When to Use Pydantic

- ✅ Building APIs (especially with FastAPI)
- ✅ Configuration file validation
- ✅ Data science ML pipelines
- ✅ Any production-grade Python code
- ✅ Parsing external data (JSON, forms, APIs)

### Best Practices

1. **Always use Pydantic V2** (not V1)
2. **Import from typing** for complex types (`List`, `Dict`, `Optional`)
3. **Use Field()** for validation constraints and metadata
4. **Use built-in types** (EmailStr, AnyUrl) when available
5. **Set sensible defaults** for optional fields
6. **Add descriptions** for better documentation

### Common Patterns

**Required fields**:

```python
name: str
age: int
```

**Optional fields**:

```python
allergies: Optional[List[str]] = None
is_married: Optional[bool] = False
```

**Fields with validation**:

```python
age: int = Field(gt=0, lt=120)
email: EmailStr
```

**Fields with metadata**:

```python
name: str = Field(max_length=50, description="Patient name")
```

---

## Next Steps

In FastAPI Section, you'll see how Pydantic models:

- Automatically validate API request bodies
- Generate API documentation
- Provide type safety across your application
- Make your code cleaner and more maintainable

---

## Summary Table

| **Feature** | **Without Pydantic** | **With Pydantic** |
| --- | --- | --- |
| Type checking | Manual `type()` checks | Automatic |
| Data validation | Manual if statements | Declarative with `Field()` |
| Code duplication | High (repeat in every function) | Low (define once) |
| Maintainability | Hard to update | Easy (change model only) |
| Type conversion | Manual | Automatic (when safe) |
| Error messages | Custom | Built-in and clear |
| Documentation | Separate docs needed | Self-documenting |

---

**Remember**: Pydantic is not just for FastAPI - it's a general-purpose validation library that makes Python code more robust and production-ready!
