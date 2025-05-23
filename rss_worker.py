import time
import feedparser
from datetime import datetime

FEEDS = [
    "https://www.respirework.com/rss/empyrean-series.xml",
    "https://www.respirework.com/rss/rebecca-yarros.xml"
]

def fetch_and_debug():
    print(f"Running at {datetime.utcnow().isoformat()} UTC")
    for url in FEEDS:
        print(f"Fetching: {url}")
        feed = feedparser.parse(url)
        print(f"Feed title: {feed.feed.get('title', 'No title')}")
        print(f"Number of entries: {len(feed.entries)}")
        for entry in feed.entries:
            print(f"- {entry.title} ({entry.link})")
        print("-" * 50)

if __name__ == "__main__":
    while True:
        fetch_and_debug()
        time.sleep(1)
