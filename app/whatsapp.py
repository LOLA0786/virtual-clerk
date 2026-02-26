from twilio.rest import Client

ACCOUNT_SID = "PASTE_ACCOUNT_SID"
AUTH_TOKEN = "PASTE_AUTH_TOKEN"

FROM = "whatsapp:+14155238886"   # Twilio sandbox
TO = "whatsapp:+91XXXXXXXXXX"    # your phone number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_message(text):
    client.messages.create(
        from_=FROM,
        to=TO,
        body=text
    )
