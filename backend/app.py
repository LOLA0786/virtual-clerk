from fastapi import FastAPI
import json
from pathlib import Path

DATA = Path("data")
DATA.mkdir(exist_ok=True)

LAWYERS = DATA / "lawyers.json"

app = FastAPI()

def load_lawyers():

    if not LAWYERS.exists():
        return []

    return json.loads(LAWYERS.read_text())

def save_lawyers(lawyers):

    LAWYERS.write_text(json.dumps(lawyers,indent=2))

@app.get("/")
def root():
    return {"product":"Virtual Clerk"}

@app.post("/signup")
def signup(name:str,email:str):

    lawyers = load_lawyers()

    lawyers.append({
        "id":len(lawyers)+1,
        "name":name,
        "email":email,
        "advocates":[]
    })

    save_lawyers(lawyers)

    return {"status":"created"}

@app.post("/track")
def track(lawyer_id:int,advocate_name:str):

    lawyers = load_lawyers()

    for l in lawyers:

        if l["id"]==lawyer_id:
            l["advocates"].append(advocate_name)

    save_lawyers(lawyers)

    return {"status":"tracking"}

@app.get("/lawyers")
def list_lawyers():

    return load_lawyers()
