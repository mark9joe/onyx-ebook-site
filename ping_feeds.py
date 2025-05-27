import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime
import os
import time

FEED_LIST_FILE = "rss_feed_list.txt"

def ping_twingly(feed_url):
    url = "https://www.twingly.com/ping"
    data = {'url': feed_url}
    try:
        response = requests.post(url, data=data, timeout=10)
        log = f"[{datetime.utcnow().isoformat()} UTC] Twingly ping for {feed_url}: {response.status_code}"
    except Exception as e:
        log = f"[{datetime.utcnow().isoformat()} UTC] Error pinging {feed_url}: {e}"
    return log

def send_email(log_content):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("EMAIL_RECIPIENT")

    if not sender or not password or not recipient:
        print("Email environment variables not set. Skipping email send.")
        return

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
    try:
        with open(FEED_LIST_FILE, "r") as f:
            feeds = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Feed list file '{FEED_LIST_FILE}' not found.")
        return

    all_logs = []
    for feed in feeds:
        log_entry = ping_twingly(feed)
        print(log_entry)
        all_logs.append(log_entry)
        time.sleep(0.2)  # throttle requests

    if all_logs:
        send_email("\n".join(all_logs))

if __name__ == "__main__":
    main()
