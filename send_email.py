import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

# Load environment variables from .env file
load_dotenv()

# 1) Load your credentials from environment variables
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")  # e.g. "you@gmail.com"
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # your 16-char
app password

# 2) Build the email
msg = EmailMessage()
msg["Subject"] = "Subject"
msg["From"] = GMAIL_ADDRESS
msg["To"] = "borowski.cacper@gmail.com"
msg.set_content("""\
Hi there,

This jdfkajsdklfjsdjf  was sent programmatically via Gmail's SMTP server!
""")

# 3) Connect to Gmail's SMTP server & send
with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    # smtp.set_debuglevel(1)
    smtp.ehlo()               # Say "hello" to the server
    smtp.starttls()           # Upgrade to encrypted connection
    smtp.ehlo()
    smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
    smtp.send_message(msg)