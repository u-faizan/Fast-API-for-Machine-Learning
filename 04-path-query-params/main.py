from fastapi import FastAPI,Path,HTTPException,Query
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

@app.get("/view")
def view():
    data = load_data()
    return data 


#without path parameters
''' 
@app.get("/patient/{patient_id}")
def view_patient(patient_id : int):  # :int is for type hinting it is not required  
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
'''
        


# using path parameters with type hinting
'''
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


        '''

# using path parameters with type hinting and HTTPException
@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the database",
        example="P001")
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



    