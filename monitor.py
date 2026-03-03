import os
import requests
import smtplib
from email.mime.text import MIMEText

URL = "https://testcisia.it/calendario.php?tolc=cents&l=gb&lingua=inglese"
EMAIL = os.environ.get("EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

def check_page():
    try:
        response = requests.get(URL, timeout=10)
        content = response.text
    except Exception as e:
        send_email("Page Monitor Error", f"Failed to fetch page: {str(e)}")
        return

    try:
        with open("old.txt", "r") as f:
            old = f.read()
    except FileNotFoundError:
        old = ""

    # Sirf tab email bhejna jab change detect ho
    if old and old != content:
        send_email("🔔 Page Changed!", f"Changes detected on:\n{URL}")
        print("✅ Email sent - page change detected!")
    else:
        print("✅ No changes detected")

    # Har run ke baad latest content save karna
    with open("old.txt", "w") as f:
        f.write(content)

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, APP_PASSWORD)
            server.sendmail(EMAIL, [EMAIL], msg.as_string())
        print(f"✅ Email sent: {subject}")
    except Exception as e:
        print(f"❌ Email send failed: {str(e)}")

if __name__ == "__main__":
    check_page()
    send_email("Test Email", "This is a test email from GitHub Actions")
