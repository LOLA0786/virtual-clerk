# ⚖️ Virtual Clerk

AI-powered Court Intelligence CLI for lawyers.

## 🚀 What it does

- Track hearing dates
- Detect judge & bench changes
- Monitor case stage updates
- Alert meaningful changes
- Prevent missed hearings

## 🧠 Why this matters

Missing one hearing can damage reputation.

Virtual Clerk acts as a digital litigation assistant.

## ⚙️ Commands

Add case:
python vc.py add CASE_NO COURT

Check alerts:
python vc.py alerts

## 🛠 Tech Stack

- Python
- Typer CLI
- JSON persistence
- Change detection engine

## 🔮 Coming Soon

- Live court data integration
- WhatsApp alerts
- Compliance deadline tracking
- Order PDF intelligence

Built in Mumbai 🇮🇳

## ⚡ Quick Start

```bash
git clone https://github.com/LOLA0786/virtual-clerk.git
cd virtual-clerk
python3 -m venv venv
source venv/bin/activate
pip install typer rich
python vc.py alerts
