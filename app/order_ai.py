from app.orders import extract_text

def summarize_order(file):
    text = extract_text(file)

    # placeholder for AI model call
    return {
        "summary": text[:200],
        "compliance": "Compliance directions detected",
        "risk": "Check compliance deadlines carefully"
    }
