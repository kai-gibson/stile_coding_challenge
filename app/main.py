from fastapi import FastAPI

app = FastAPI()

@app.post("/import")
def import_marks():
    return {"testing":"data"}
