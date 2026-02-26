import typer
from rich import print
from app.fetch import fetch_bench_pdfs
from app.listing import find_listing

app = typer.Typer(help="⚖️ Virtual Clerk")

@app.command()
def listing(case_number: str):
    """Check if case is listed"""
    print("\nFetching cause lists...\n")
    fetch_bench_pdfs()

    results = find_listing(case_number)

    if not results:
        print("❌ Not listed")
        return

    for r in results:
        print("[bold green]LISTED[/bold green]\n")
        print("Court:", r["bench"]["court"])
        print("Bench:")
        for j in r["bench"]["bench"]:
            print("  ", j)
        print("Time:", r["bench"]["time"])
        print("Sequence:", r["sequence"])
        print("Entry:", r["line"])
        print()

@app.command()
def version():
    """Show version"""
    print("VC v0.1")

if __name__ == "__main__":
    app()
