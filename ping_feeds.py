import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime
import os

FEEDS = [
    "https://www.respirework.com/rss/empyrean-series.xml"
]

def ping_twingly(feed_url):
    url = "https://www.twingly.com/ping"
    data = {'url': feed_url}
    try:
        response = requests.post(url, data=data)
        log = f"[{datetime.utcnow().isoformat()} UTC] Twingly ping for {feed_url}: {response.status_code}"
    except Exception as e:
        log = f"[{datetime.utcnow().isoformat()} UTC] Error pinging {feed_url}: {e}"
    return log

def send_email(log_content):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("EMAIL_RECIPIENT")

    msg = MIMEText(log_content)
    msg["Subject"] = "RSS Ping Log - respirework.com"
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print("Log email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    all_logs = []
    for feed in FEEDS:
        result = ping_twingly(feed)
        print(result)
        all_logs.append(result)
    send_email("\n".join(all_logs))

if __name__ == "__main__":
    main()
