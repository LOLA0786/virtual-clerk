from fastapi import FastAPI
from typing import Dict, List

app = FastAPI(title="Virtual Clerk Litigation API")

# ---- mock data layer ----

cases = {
    "ABC123": {
        "case_number": "ABC123",
        "court": "Bombay High Court",
        "judge": "Justice Kulkarni",
        "next_hearing": "2026-03-15",
        "status": "Pending"
    }
}

hearings = [
    {
        "case_number": "ABC123",
        "court": "Court 32",
        "time": "11:00",
        "judge": "Justice Kulkarni"
    }
]

# ---- APIs ----

@app.get("/")
def root():
    return {"service": "virtual clerk litigation api"}

@app.get("/case/{case_number}")
def get_case(case_number: str):
    return cases.get(case_number, {"error": "case not found"})

@app.get("/hearings/today")
def today_hearings():
    return hearings

@app.get("/health")
def health():
    return {"status": "ok"}
