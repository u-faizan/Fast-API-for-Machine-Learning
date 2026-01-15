from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return "Message : Hello World"


@app.get("/about")
def about():
    return {
"message": "Campus X is an education platform where you can learn AI"
    }