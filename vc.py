import typer
import json
from pathlib import Path
from datetime import datetime, timedelta
import random

app = typer.Typer()

DATA_FILE = Path("data/cases.json")

CRITICAL_FIELDS = ["next_date", "judge", "stage"]
MINOR_FIELDS = ["courtroom"]


def load_cases():
    if not DATA_FILE.exists():
        return {}
    return json.loads(DATA_FILE.read_text())


def save_cases(cases):
    DATA_FILE.write_text(json.dumps(cases, indent=2))


def fetch_case_status(case_no, court):
    judges = ["Justice Kulkarni", "Justice Mehta", "Justice Patel"]
    stages = ["Admission", "Final Arguments", "Reply", "Orders Reserved"]

    next_date = datetime.today() + timedelta(days=random.randint(3, 20))

    return {
        "next_date": next_date.strftime("%d-%b-%Y"),
        "judge": random.choice(judges),
        "stage": random.choice(stages),
        "courtroom": random.randint(10, 60),
    }


def detect_changes(old, new):
    critical = []
    minor = []

    for key in new:
        if old.get(key) != new[key]:
            if key in CRITICAL_FIELDS:
                critical.append(f"{key} → {new[key]}")
            elif key in MINOR_FIELDS:
                minor.append(f"{key} → {new[key]}")
    return critical, minor


@app.command()
def alerts():
    """Detect meaningful changes"""
    cases = load_cases()

    typer.echo("\n🔔 Change Alerts:\n")

    for case_no, info in cases.items():
        new_status = fetch_case_status(case_no, info["court"])
        old_status = info.get("last_status", {})

        critical, minor = detect_changes(old_status, new_status)

        if critical or minor:
            typer.echo(f"⚖️ {case_no}")

            for c in critical:
                typer.echo(f"  🚨 {c}")

            for m in minor:
                typer.echo(f"  ℹ {m}")

            typer.echo("")

        cases[case_no]["last_status"] = new_status

    save_cases(cases)
    typer.echo("✔ Smart check complete.\n")


@app.command()
def version():
    typer.echo("VC v0.2")


if __name__ == "__main__":
    app()
