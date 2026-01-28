# Pydantic Crash Course | Data Validation in Python

## Overview

This crash course covers **Pydantic** - a powerful Python library for data validation and type enforcement. Pydantic is essential for production-grade code, especially when working with FastAPI, ML pipelines, and configuration management.

**Key Topics Covered:**
1. Why Pydantic is needed
2. Type validation and data validation
3. Pydantic models and schemas
4. Field validators and model validators
5. Computed fields and nested models
6. Exporting models to dictionaries/JSON

---

## Why Pydantic?

### The Problem with Python's Dynamic Typing

Python is a **dynamically typed language** - you can store different types of values in the same variable:

```python
x = 10        # Integer
x = "hello"   # String - this works!
```

**Issues:**
- ✅ Great for beginners
- ❌ Problematic for production-grade code
- ❌ No built-in type enforcement
- ❌ Requires manual validation code

---

## Problems Pydantic Solves

### Problem #1: Type Validation

**Scenario: Function Without Type Validation**

```python
def insert_patient_data(name, age):
    """Insert patient data into database"""
    print(name)
    print(age)
    print("Inserting into database...")

# Junior programmer calls the function
insert_patient_data("Nitish", "30")  # ❌ Age is string, not integer!
```

**Issues:**
- Function expects `age` to be an integer
- Code accepts string without error
- Wrong data type gets inserted into database
- No enforcement of data types

**Attempted Solution: Type Hinting**

```python
def insert_patient_data(name: str, age: int):
    print(name)
    print(age)
    print("Inserting into database...")

insert_patient_data("Nitish", "30")  # Still works! ❌
```

**Problem:** Type hints don't produce errors - they're just suggestions for developers.

**Manual Validation Approach**

```python
def insert_patient_data(name: str, age: int):
    # Manual type checking
    if type(name) != str or type(age) != int:
        raise TypeError("Incorrect data type")
    
    print(name)
    print(age)
    print("Inserting into database...")

insert_patient_data("Nitish", "30")  # ✓ Now raises TypeError
```

**Why This Approach Doesn't Scale:**
- ❌ Must write validation code in every function
- ❌ Must update validation if new fields are added
- ❌ Repetitive boilerplate code
- ❌ Hard to maintain

---

### Problem #2: Data Validation

**Scenario: Business Logic Constraints**

```python
def insert_patient_data(name: str, age: int):
    # Type validation
    if type(name) != str or type(age) != int:
        raise TypeError("Incorrect data type")
    
    # Data validation
    if age < 0:
        raise ValueError("Age can't be negative")
    
    print(name)
    print(age)
    print("Inserting into database...")
```

**Scaling Problems:**
- Need validation for email format
- Need validation for phone numbers
- Need validation for each of 10+ fields
- Must duplicate all validation in update functions

**This is where Pydantic comes in!**

---

## How Pydantic Works

### Three-Step Process

**Step 1: Build a Pydantic Model**
- Define a class that inherits from `BaseModel`
- Specify fields and their data types
- Add validation constraints

**Step 2: Create Object with Raw Data**
- Pass raw dictionary to the model
- Automatic validation happens
- Get a validated Pydantic object

**Step 3: Use Validated Object**
- Pass validated object to your function
- No manual validation needed
- Clean, maintainable code

---

## Installation

```bash
pip install pydantic

# Make sure to install Pydantic V2 (recommended)
# V2 is written in Rust and much faster
```

**Version Differences:**
- **Pydantic V1**: Older version
- **Pydantic V2**: Current recommended version (faster, more features)

---

## Creating Your First Pydantic Model

### Step 1: Import and Define Model

```python
from pydantic import BaseModel

class Patient(BaseModel):
    """Pydantic model for patient data"""
    name: str
    age: int
```

**Key Points:**
- Must inherit from `BaseModel`
- Define fields with type annotations
- This creates the schema for your data

---

### Step 2: Create Pydantic Object

```python
# Raw data from user
patient_info = {
    "name": "Nitish",
    "age": 30
}

# Create validated Pydantic object
patient1 = Patient(**patient_info)

print(patient1)
# Output: name='Nitish' age=30
```

**What Happens:**
- Pydantic validates all types automatically
- If validation passes → creates object
- If validation fails → raises error

---

### Step 3: Use in Functions

```python
def insert_patient_data(patient: Patient):
    """Insert patient data into database"""
    print(patient.name)
    print(patient.age)
    print("Inserting into database...")

# Call function with validated object
insert_patient_data(patient1)
```

**Benefits:**
- ✅ No manual validation code
- ✅ Type-safe function signature
- ✅ Access fields with dot notation
- ✅ Clean, readable code

---

## Type Validation in Action

### Valid Data

```python
patient_info = {
    "name": "Nitish",
    "age": 30  # Integer - correct type
}

patient1 = Patient(**patient_info)
# ✓ Works perfectly
```

### Invalid Data

```python
patient_info = {
    "name": "Nitish",
    "age": "THIRTY"  # String instead of integer
}

patient1 = Patient(**patient_info)
# ❌ Raises ValidationError
```

**Error Message:**
```
ValidationError: 1 validation error for Patient
age
  Input should be a valid integer
```

---

## Automatic Type Coercion

Pydantic is **smart enough** to convert compatible types:

```python
patient_info = {
    "name": "Nitish",
    "age": "30"  # String that can be converted to int
}

patient1 = Patient(**patient_info)
# ✓ Works! Pydantic converts "30" to 30
```

**Pydantic automatically converts:**
- `"30"` (string) → `30` (integer)
- `"3.14"` (string) → `3.14` (float)
- `"true"` (string) → `True` (boolean)

---

## Complex Data Types

### Working with Lists and Dictionaries

```python
from pydantic import BaseModel
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    bmi: float
    married: bool
    allergies: List[str]  # List of strings
    contact_details: Dict[str, str]  # Dictionary with string keys and values
```

**Why use `List[str]` instead of `list`?**
- `list` only validates that it's a list
- `List[str]` validates it's a list AND each item is a string
- Provides **two-level validation**

---

### Creating Complex Pydantic Objects

```python
patient_info = {
    "name": "Nitish",
    "age": 30,
    "weight": 75.2,
    "height": 1.75,
    "bmi": 24.5,
    "married": True,
    "allergies": ["Pollen", "Dust"],
    "contact_details": {
        "email": "abc@gmail.com",
        "phone": "1234567890"
    }
}

patient1 = Patient(**patient_info)
```

**Validation:**
- Checks if `allergies` is a list ✓
- Checks if each item in list is a string ✓
- Checks if `contact_details` is a dictionary ✓
- Checks if all keys and values are strings ✓

---

## Required vs Optional Fields

### Required Fields (Default)

By default, **all fields are required**:

```python
class Patient(BaseModel):
    name: str      # Required
    age: int       # Required
    weight: float  # Required

patient_info = {
    "name": "Nitish",
    "age": 30
    # weight missing!
}

patient1 = Patient(**patient_info)
# ❌ ValidationError: field required
```

---

### Optional Fields

Make fields optional using `Optional`:

```python
from typing import Optional, List

class Patient(BaseModel):
    name: str                        # Required
    age: int                         # Required
    weight: float                    # Required
    allergies: Optional[List[str]] = None  # Optional with default None
    married: Optional[bool] = None         # Optional with default None
```

**Key Points:**
- Import `Optional` from `typing`
- Syntax: `Optional[Type] = default_value`
- Default value is usually `None`

---

### Setting Custom Default Values

```python
class Patient(BaseModel):
    name: str
    age: int
    married: bool = False  # Default value is False

patient_info = {
    "name": "Nitish",
    "age": 30
    # married not provided
}

patient1 = Patient(**patient_info)
print(patient1.married)  # Output: False
```

---

## Data Validation with Custom Types

### Built-in Custom Types

Pydantic provides special types for common validation scenarios:

### EmailStr - Email Validation

```python
from pydantic import BaseModel, EmailStr

class Patient(BaseModel):
    name: str
    email: EmailStr  # Validates email format

patient_info = {
    "name": "Nitish",
    "email": "abc@gmail.com"  # Valid email
}

patient1 = Patient(**patient_info)  # ✓ Works
```

**Invalid Email:**

```python
patient_info = {
    "name": "Nitish",
    "email": "abcgmail.com"  # Missing @
}

patient1 = Patient(**patient_info)
# ❌ ValidationError: value is not a valid email address
```

---

### AnyUrl - URL Validation

```python
from pydantic import BaseModel, AnyUrl

class Patient(BaseModel):
    name: str
    linkedin_url: AnyUrl  # Validates URL format

patient_info = {
    "name": "Nitish",
    "linkedin_url": "https://linkedin.com/in/nitish"  # Valid URL
}

patient1 = Patient(**patient_info)  # ✓ Works
```

**Invalid URL:**

```python
patient_info = {
    "name": "Nitish",
    "linkedin_url": "linkedin.com"  # Missing https://
}

patient1 = Patient(**patient_info)
# ❌ ValidationError: invalid or missing URL scheme
```

---

## Field() Function for Advanced Validation

### Purpose of Field()

The `Field()` function provides:
1. **Custom data validation** (min, max, length constraints)
2. **Metadata** (descriptions, examples, titles)
3. **Default values**
4. **Type coercion control**

### Importing Field

```python
from pydantic import BaseModel, Field
```

---

### Numeric Constraints

```python
class Patient(BaseModel):
    name: str
    age: int = Field(gt=0, lt=120)  # Greater than 0, less than 120
    weight: float = Field(gt=0)     # Greater than 0
    height: float = Field(gt=0)     # Greater than 0
```

**Available Constraints:**
- `gt` - Greater than
- `ge` - Greater than or equal to
- `lt` - Less than
- `le` - Less than or equal to

**Testing:**

```python
patient_info = {
    "name": "Nitish",
    "age": 130,  # Exceeds max
    "weight": 75.2,
    "height": 1.75
}

patient1 = Patient(**patient_info)
# ❌ ValidationError: Input should be less than 120
```

---

### String Constraints

```python
class Patient(BaseModel):
    name: str = Field(max_length=50)  # Maximum 50 characters
    email: EmailStr

patient_info = {
    "name": "A" * 60,  # 60 characters - too long!
    "email": "abc@gmail.com"
}

patient1 = Patient(**patient_info)
# ❌ ValidationError: String should have at most 50 characters
```

**Available String Constraints:**
- `min_length` - Minimum string length
- `max_length` - Maximum string length
- `pattern` - Regex pattern validation

---

### List Constraints

```python
from typing import List

class Patient(BaseModel):
    name: str
    allergies: List[str] = Field(max_length=5)  # Maximum 5 allergies

patient_info = {
    "name": "Nitish",
    "allergies": ["Pollen", "Dust", "Cats", "Dogs", "Grass", "Peanuts"]  # 6 items!
}

patient1 = Patient(**patient_info)
# ❌ ValidationError: List should have at most 5 items
```

---

## Adding Metadata with Field()

### Purpose of Metadata

Metadata helps:
- Document your API
- Provide examples for users
- Generate better auto-documentation (FastAPI)
- Improve code readability

### Using Annotated for Metadata

```python
from pydantic import BaseModel, Field
from typing import Annotated

class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Patient Name",
            description="Give the name of the patient in less than 50 characters",
            examples=["Nitish", "Amit"]
        )
    ]
    age: Annotated[
        int,
        Field(
            gt=0,
            lt=120,
            title="Patient Age",
            description="Age of the patient"
        )
    ]
```

**What Annotated Does:**
- First argument: Data type
- Second argument: Field function with constraints and metadata
- Combines type hints with validation and documentation

---

### Default Values with Field()

```python
class Patient(BaseModel):
    name: str
    married: Annotated[
        bool,
        Field(
            default=False,
            description="Is the patient married?"
        )
    ]

patient_info = {"name": "Nitish"}
patient1 = Patient(**patient_info)
print(patient1.married)  # Output: False
```

---

## Strict Type Validation

### The Problem: Type Coercion

By default, Pydantic converts compatible types:

```python
class Patient(BaseModel):
    weight: float

patient_info = {"weight": "75.2"}  # String
patient1 = Patient(**patient_info)
# ✓ Works - Pydantic converts "75.2" to 75.2
```

**Sometimes you don't want this behavior!**

---

### Using strict=True

```python
class Patient(BaseModel):
    weight: Annotated[
        float,
        Field(gt=0, strict=True)  # Disable type coercion
    ]

patient_info = {"weight": "75.2"}  # String
patient1 = Patient(**patient_info)
# ❌ ValidationError: Input should be a valid number

patient_info = {"weight": 75.2}  # Float
patient1 = Patient(**patient_info)
# ✓ Works
```

**Use Cases for strict=True:**
- Financial data (no string-to-number conversion)
- IDs that must be specific types
- When you want exact type matching

---

## Field Validators

### What Are Field Validators?

**Field Validators** allow you to:
1. Apply **custom business logic** validation
2. Perform **data transformations**
3. Validate based on **specific requirements**

### When to Use Field Validators

Use field validators when:
- Built-in types (EmailStr, AnyUrl) don't fit your needs
- You need business-specific validation
- Field() constraints aren't sufficient

---

### Example: Email Domain Validation

**Scenario:** Hospital only accepts employees from HDFC Bank and ICICI Bank (identified by email domain).

```python
from pydantic import BaseModel, EmailStr, field_validator

class Patient(BaseModel):
    name: str
    email: EmailStr
    
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        """Validate that email is from allowed domains"""
        valid_domains = ["hdfc.com", "icici.com"]
        
        # Extract domain from email
        domain = value.split("@")[1]
        
        # Check if domain is valid
        if domain not in valid_domains:
            raise ValueError("Not a valid domain")
        
        return value
```

**Code Breakdown:**
- `@field_validator('email')` - Applies to email field
- `@classmethod` - Required decorator
- `cls` - Class instance
- `value` - Current value of the field
- Must return the value if valid
- Raise `ValueError` if invalid

---

### Testing Email Validator

**Valid Email:**

```python
patient_info = {
    "name": "Nitish",
    "email": "nitish@hdfc.com"  # Valid domain
}

patient1 = Patient(**patient_info)
# ✓ Works
```

**Invalid Email:**

```python
patient_info = {
    "name": "Nitish",
    "email": "nitish@gmail.com"  # Invalid domain
}

patient1 = Patient(**patient_info)
# ❌ ValueError: Not a valid domain
```

---

### Example: Data Transformation

**Scenario:** Always capitalize patient names.

```python
class Patient(BaseModel):
    name: str
    email: EmailStr
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        """Transform name to uppercase"""
        return value.upper()

patient_info = {
    "name": "nitish",
    "email": "nitish@hdfc.com"
}

patient1 = Patient(**patient_info)
print(patient1.name)  # Output: NITISH
```

---

## Field Validator Modes

### Understanding Before vs After Mode

Field validators operate in two modes:

**after mode (default):**
- Validation runs **after** type coercion
- You receive the value after Pydantic converts it

**before mode:**
- Validation runs **before** type coercion
- You receive the raw value as provided

---

### Example: Age Validation

**Scenario:** Validate age is between 0 and 100.

```python
class Patient(BaseModel):
    name: str
    age: int
    
    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, value):
        """Validate age range"""
        if value > 0 and value < 100:
            return value
        else:
            raise ValueError("Age should be between 0 and 100")
```

**Testing with before mode:**

```python
patient_info = {
    "name": "Nitish",
    "age": "30"  # String
}

patient1 = Patient(**patient_info)
# ❌ Error: can't compare string and integer
# Receives "30" (string) before conversion
```

---

**Using after mode:**

```python
class Patient(BaseModel):
    name: str
    age: int
    
    @field_validator('age', mode='after')  # or just omit mode
    @classmethod
    def validate_age(cls, value):
        """Validate age range"""
        if value > 0 and value < 100:
            return value
        else:
            raise ValueError("Age should be between 0 and 100")

patient_info = {
    "name": "Nitish",
    "age": "30"  # String
}

patient1 = Patient(**patient_info)
# ✓ Works! Receives 30 (integer) after conversion
```

**Summary:**
- `mode='after'` (default) - Best for most cases
- `mode='before'` - Use when you need to validate raw input

---

## Model Validators

### What Are Model Validators?

**Model Validators** allow validation across **multiple fields** at once.

**Use When:**
- Validation depends on multiple fields
- You need cross-field validation logic
- Business rules involve field relationships

---

### Example: Emergency Contact Validation

**Scenario:** Patients over 60 must provide an emergency contact number.

```python
from pydantic import BaseModel, model_validator
from typing import Dict

class Patient(BaseModel):
    name: str
    age: int
    contact_details: Dict[str, str]
    
    @model_validator(mode='after')
    @classmethod
    def validate_emergency_contact(cls, model):
        """Validate emergency contact for patients over 60"""
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("Patient older than 60 must have an emergency contact")
        return model
```

**Code Breakdown:**
- `@model_validator(mode='after')` - Validates after all fields are processed
- Receives entire `model` object (not just one field)
- Access any field with `model.field_name`
- Must return the model

---

### Testing Model Validator

**Invalid - No Emergency Contact:**

```python
patient_info = {
    "name": "Nitish",
    "age": 65,
    "contact_details": {
        "phone": "1234567890"
    }
}

patient1 = Patient(**patient_info)
# ❌ ValueError: Patient older than 60 must have an emergency contact
```

**Valid - Emergency Contact Provided:**

```python
patient_info = {
    "name": "Nitish",
    "age": 65,
    "contact_details": {
        "phone": "1234567890",
        "emergency": "9876543210"  # Emergency contact added
    }
}

patient1 = Patient(**patient_info)
# ✓ Works
```

**Valid - Under 60:**

```python
patient_info = {
    "name": "Nitish",
    "age": 30,
    "contact_details": {
        "phone": "1234567890"
    }
}

patient1 = Patient(**patient_info)
# ✓ Works - no emergency contact needed
```

---

## Computed Fields

### What Are Computed Fields?

**Computed Fields** are fields whose values are **calculated dynamically** from other fields, not provided by the user.

**Characteristics:**
- Not user-provided
- Calculated from other fields
- Read-only
- Auto-updated based on dependencies

---

### Example: BMI Calculation

**Scenario:** Calculate BMI from weight and height.

```python
from pydantic import BaseModel, computed_field

class Patient(BaseModel):
    name: str
    weight: float  # in kg
    height: float  # in meters
    
    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI from weight and height"""
        bmi_value = self.weight / (self.height ** 2)
        return round(bmi_value, 2)
```

**Code Breakdown:**
- `@computed_field` - Marks field as computed
- `@property` - Makes it accessible like an attribute
- `-> float` - Return type annotation
- Access other fields with `self.field_name`
- Calculation happens automatically

---

### Using Computed Fields

```python
patient_info = {
    "name": "Nitish",
    "weight": 75.0,
    "height": 1.72
}

patient1 = Patient(**patient_info)

print(patient1.name)    # Output: Nitish
print(patient1.weight)  # Output: 75.0
print(patient1.height)  # Output: 1.72
print(patient1.bmi)     # Output: 25.35 (calculated automatically)
```

**Note:** Users only provide name, weight, and height. BMI is calculated automatically!

---

## Nested Models

### What Are Nested Models?

**Nested Models** are Pydantic models used as fields within other Pydantic models.

**Benefits:**
1. **Better organization** - Logical data grouping
2. **Reusability** - Use same model in multiple places
3. **Readability** - Clear data structure
4. **Automatic validation** - Validates nested structures

---

### Example: Patient with Address

**Problem:** Address is complex data with multiple components (city, state, PIN code).

**Solution:** Create separate model for Address.

```python
from pydantic import BaseModel

class Address(BaseModel):
    """Model for address data"""
    city: str
    state: str
    pin_code: str

class Patient(BaseModel):
    """Model for patient data"""
    name: str
    gender: str
    age: int
    address: Address  # Nested model
```

---

### Creating Nested Model Objects

**Step 1: Create Address Object**

```python
address_dict = {
    "city": "Gurgaon",
    "state": "Haryana",
    "pin_code": "122001"
}

address1 = Address(**address_dict)
```

**Step 2: Create Patient Object with Address**

```python
patient_dict = {
    "name": "Nitish",
    "gender": "Male",
    "age": 30,
    "address": address1  # Pass address object
}

patient1 = Patient(**patient_dict)
```

---

### Accessing Nested Data

```python
print(patient1.name)              # Output: Nitish
print(patient1.address.city)      # Output: Gurgaon
print(patient1.address.pin_code)  # Output: 122001

# Full patient object
print(patient1)
# Output:
# name='Nitish' gender='Male' age=30 
# address=Address(city='Gurgaon', state='Haryana', pin_code='122001')
```

---

### Benefits of Nested Models

**1. Reusability**

```python
class Employee(BaseModel):
    name: str
    employee_id: str
    address: Address  # Reuse Address model

class Student(BaseModel):
    name: str
    roll_number: str
    address: Address  # Reuse Address model
```

**2. Better Organization**

```
Patient
├── name
├── gender
├── age
└── address
    ├── city
    ├── state
    └── pin_code
```

**3. Automatic Validation**

- Address fields are automatically validated
- Type checking happens for nested structures
- Constraints apply to nested models

---

## Exporting Pydantic Models

### Why Export Models?

Common use cases:
- **API responses** - Send data to frontend
- **Database operations** - Store in database
- **Debugging** - Inspect model data
- **Logging** - Record model state
- **Serialization** - Save to files

---

### Export to Dictionary

**Using model_dump():**

```python
class Patient(BaseModel):
    name: str
    age: int

patient1 = Patient(name="Nitish", age=30)

# Export to dictionary
patient_dict = patient1.model_dump()

print(patient_dict)  # Output: {'name': 'Nitish', 'age': 30}
print(type(patient_dict))  # Output: <class 'dict'>
```

---

### Export to JSON

**Using model_dump_json():**

```python
patient1 = Patient(name="Nitish", age=30)

# Export to JSON string
patient_json = patient1.model_dump_json()

print(patient_json)  # Output: '{"name":"Nitish","age":30}'
print(type(patient_json))  # Output: <class 'str'>
```

---

## Advanced Export Options

### Include Specific Fields

```python
class Patient(BaseModel):
    name: str
    age: int
    gender: str

patient1 = Patient(name="Nitish", age=30, gender="Male")

# Export only name field
patient_dict = patient1.model_dump(include=['name'])
print(patient_dict)  # Output: {'name': 'Nitish'}

# Export multiple specific fields
patient_dict = patient1.model_dump(include=['name', 'age'])
print(patient_dict)  # Output: {'name': 'Nitish', 'age': 30}
```

---

### Exclude Specific Fields

```python
# Export everything except name and gender
patient_dict = patient1.model_dump(exclude=['name', 'gender'])
print(patient_dict)  # Output: {'age': 30}
```

---

### Exclude from Nested Models

```python
class Address(BaseModel):
    city: str
    state: str
    pin_code: str

class Patient(BaseModel):
    name: str
    age: int
    address: Address

patient1 = Patient(
    name="Nitish",
    age=30,
    address=Address(city="Gurgaon", state="Haryana", pin_code="122001")
)

# Exclude state from nested address
patient_dict = patient1.model_dump(exclude={'address': ['state']})

print(patient_dict)
# Output: 
# {
#     'name': 'Nitish',
#     'age': 30,
#     'address': {'city': 'Gurgaon', 'pin_code': '122001'}
# }
```

---

### Exclude Unset Fields

```python
class Patient(BaseModel):
    name: str
    age: int
    gender: str = "Male"  # Default value

# Create patient without setting gender
patient_info = {
    "name": "Nitish",
    "age": 30
    # gender not provided - will use default
}

patient1 = Patient(**patient_info)

# Export without fields that weren't explicitly set
patient_dict = patient1.model_dump(exclude_unset=True)

print(patient_dict)  # Output: {'name': 'Nitish', 'age': 30}
# Gender excluded because it wasn't explicitly set (used default)
```

**Use Case:** Useful for updates where you only want to export fields the user actually provided.

---

## Summary of Export Options

| **Parameter** | **Purpose** | **Example** |
|---|---|---|
| `include` | Export only specific fields | `model_dump(include=['name', 'age'])` |
| `exclude` | Exclude specific fields | `model_dump(exclude=['password'])` |
| `exclude_unset` | Exclude fields not explicitly set | `model_dump(exclude_unset=True)` |
| `exclude_none` | Exclude fields with None values | `model_dump(exclude_none=True)` |
| `exclude_defaults` | Exclude fields with default values | `model_dump(exclude_defaults=True)` |

---

## Complete Example

```python
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Address(BaseModel):
    """Model for address information"""
    city: str
    state: str
    pin_code: str

class Patient(BaseModel):
    """Comprehensive patient model with all Pydantic features"""
    
    # Basic fields with constraints
    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Patient Name",
            description="Full name of the patient"
        )
    ]
    
    age: Annotated[
        int,
        Field(gt=0, lt=120, description="Age of the patient")
    ]
    
    # Email validation
    email: EmailStr
    
    # Numeric fields with constraints
    weight: Annotated[float, Field(gt=0, description="Weight in kg")]
    height: Annotated[float, Field(gt=0, description="Height in meters")]
    
    # Optional fields
    married: bool = False
    allergies: Optional[List[str]] = Field(default=None, max_length=5)
    
    # Complex types
    contact_details: Dict[str, str]
    
    # Nested model
    address: Address
    
    # Field validator - email domain check
    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, value):
        """Validate email is from allowed domains"""
        valid_domains = ["hdfc.com", "icici.com"]
        domain = value.split("@")[1]
        if domain not in valid_domains:
            raise ValueError(f"Email must be from {valid_domains}")
        return value
    
    # Field validator - name transformation
    @field_validator('name')
    @classmethod
    def capitalize_name(cls, value):
        """Convert name to uppercase"""
        return value.upper()
    
    # Model validator - cross-field validation
    @model_validator(mode='after')
    @classmethod
    def validate_emergency_contact(cls, model):
        """Patients over 60 must have emergency contact"""
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("Patients over 60 need emergency contact")
        return model
    
    # Computed field
    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI from weight and height"""
        bmi_value = self.weight / (self.height ** 2)
        return round(bmi_value, 2)
```

---

## Key Takeaways

### Why Use Pydantic?

✅ **Eliminates manual validation code**
- No need to write type checking
- No need to write data validation
- Reduces boilerplate significantly

✅ **Type safety**
- Enforces data types
- Catches errors early
- Automatic type coercion when sensible

✅ **Data validation**
- Built-in validators (EmailStr, AnyUrl)
- Custom validators (Field function)
- Business logic validators (field_validator, model_validator)

✅ **Production-ready**
- Used extensively in FastAPI
- Battle-tested in ML pipelines
- Essential for configuration management

---

### Pydantic Features Summary

| **Feature** | **Use Case** | **Key Function** |
|---|---|---|
| **BaseModel** | Create data schemas | Inherit from `BaseModel` |
| **Type Annotations** | Define field types | `name: str`, `age: int` |
| **Optional Fields** | Make fields optional | `Optional[Type] = default` |
| **Custom Types** | Common validations | `EmailStr`, `AnyUrl` |
| **Field()** | Constraints & metadata | `Field(gt=0, description="...")` |
| **field_validator** | Single field validation | `@field_validator('field_name')` |
| **model_validator** | Multi-field validation | `@model_validator(mode='after')` |
| **computed_field** | Calculated fields | `@computed_field @property` |
| **Nested Models** | Complex data structures | Use model as field type |
| **Export** | Serialize to dict/JSON | `model_dump()`, `model_dump_json()` |

---

### Best Practices

1. **Always use Pydantic V2** - Faster and more features
2. **Use built-in types when possible** - EmailStr, AnyUrl, etc.
3. **Add metadata** - Helps with documentation and API generation
4. **Validate early** - Use field_validator for business logic
5. **Organize with nested models** - Better structure and reusability
6. **Use strict=True** - When you need exact type matching
7. **Export selectively** - Use include/exclude to control output

---

### Common Pydantic Patterns

**Pattern 1: Required field with constraints**
```python
age: int = Field(gt=0, lt=120)
```

**Pattern 2: Optional field with default**
```python
married: bool = False
```

**Pattern 3: Field with metadata**
```python
name: Annotated[str, Field(max_length=50, description="Patient name")]
```

**Pattern 4: Custom validation**
```python
@field_validator('email')
@classmethod
def validate_email(cls, value):
    # validation logic
    return value
```

**Pattern 5: Computed field**
```python
@computed_field
@property
def full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"
```

---

### Next Steps

Now that you understand Pydantic:

1. **Practice** - Build your own Pydantic models
2. **FastAPI** - Learn how FastAPI uses Pydantic for API development
3. **Advanced Topics** - Explore serialization, custom validators, config
4. **Real Projects** - Use in ML pipelines, API development, data processing

---

## Additional Resources

**Official Documentation:**
- Pydantic V2 Docs: https://docs.pydantic.dev/

**Related Technologies:**
- FastAPI (uses Pydantic extensively)
- SQLAlchemy (can integrate with Pydantic)
- Configuration management tools

---

This crash course covers everything you need to get started with Pydantic. With this knowledge, you're ready to write production-grade Python code with proper type and data validation! 🚀