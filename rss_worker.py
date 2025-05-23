import time
import feedparser

FEEDS = [
    "https://www.respirework.com/rss/empyrean-series.xml",
    "https://www.respirework.com/rss/rebecca-yarros.xml"
]

def fetch_and_log():
    for url in FEEDS:
        print(f"Fetching: {url}")
        feed = feedparser.parse(url)
        if feed.entries:
            latest = feed.entries[0]
            print(f"Title: {latest.title}")
            print(f"Link: {latest.link}")
            print("-" * 40)
        else:
            print("No entries found.")

if __name__ == "__main__":
    while True:
        fetch_and_log()
        time.sleep(1)
