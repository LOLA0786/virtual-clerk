from fastapi import FastAPI
from models import SessionLocal, Lawyer, Advocate

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Virtual Clerk API"}

@app.post("/signup")
def signup(name: str, email: str, phone: str):

    db = SessionLocal()

    lawyer = Lawyer(name=name, email=email, phone=phone)

    db.add(lawyer)
    db.commit()

    return {"status": "lawyer created"}

@app.post("/track")
def track_advocate(lawyer_id: int, advocate_name: str):

    db = SessionLocal()

    adv = Advocate(lawyer_id=lawyer_id, advocate_name=advocate_name)

    db.add(adv)
    db.commit()

    return {"status": "tracking started"}

@app.get("/advocates")
def list_advocates():

    db = SessionLocal()

    advs = db.query(Advocate).all()

    return advs
