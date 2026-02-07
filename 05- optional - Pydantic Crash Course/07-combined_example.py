from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field, model_validator
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
        print(f"[Validator] Checking email domain: {domain}")
        if domain not in valid_domains:
            raise ValueError(f"Email must be from {valid_domains}")
        return value
    
    # Field validator - name transformation
    @field_validator('name')
    @classmethod
    def capitalize_name(cls, value):
        """Convert name to uppercase"""
        transformed = value.upper()
        print(f"[Validator] Transforming name '{value}' -> '{transformed}'")
        return transformed
    
    # Model validator - cross-field validation
    @model_validator(mode='after')
    @classmethod
    def validate_emergency_contact(cls, model):
        """Patients over 60 must have emergency contact"""
        print(f"[Model Validator] Validating emergency contact for age {model.age}")
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("Patients over 60 need emergency contact")
        return model
    
    # Computed field
    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI from weight and height"""
        bmi_value = self.weight / (self.height ** 2)
        print(f"[Computed Field] Calculating BMI: {bmi_value}")
        return round(bmi_value, 2)
    
    # Custom post-init print
    def __init__(self, **data):
        super().__init__(**data)
        print(f"[Init] Patient '{self.name}' created, age: {self.age}, BMI: {self.bmi}")

# Example usage
if __name__ == "__main__":
    patient = Patient(
        name="John Doe",
        age=65,
        email="john@hdfc.com",
        weight=70,
        height=1.75,
        contact_details={"emergency": "1234567890"},
        address=Address(city="Mumbai", state="MH", pin_code="400001")
    )
    
    print(f"Patient BMI: {patient.bmi}")
