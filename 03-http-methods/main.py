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

@app.get("/view")
def view():
    data = load_data()
    return data 
