from datetime import datetime
from app.db import load, save

def add_case(case_no, court):
    data = load()
    data[case_no] = {"court": court}
    save(data)

def list_cases():
    return load()

def mock_fetch_status():
    today = datetime.now().day

    # stable daily values
    judge = "Justice Patel" if today % 2 == 0 else "Justice Kulkarni"
    stage = "Admission" if today % 3 == 0 else "Final Hearing"
    courtroom = 30 + (today % 5)

    return {
        "next_date": datetime.now().date().isoformat(),
        "judge": judge,
        "stage": stage,
        "courtroom": courtroom
    }

def check_updates():
    data = load()
    alerts = []

    for case, info in data.items():
        new = mock_fetch_status()
        old = info.get("last_status")

        if old != new:
            alerts.append((case,new))
            info["last_status"] = new

    save(data)
    return alerts
