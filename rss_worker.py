import time
import feedparser
from datetime import datetime

FEEDS = [
    "https://www.respirework.com/rss/empyrean-series.xml",
    "https://www.respirework.com/rss/rebecca-yarros.xml"
]

OUTPUT_FILE = "public/rss-latest.html"

def fetch_and_save():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Latest RSS Updates</title>")
        f.write("<link rel='stylesheet' href='https://cdn.tailwindcss.com'><style>body{padding:2rem;font-family:sans-serif;}</style></head><body>")
        f.write("<h1 class='text-3xl font-bold mb-4'>Latest RSS Posts</h1>")

        for url in FEEDS:
            feed = feedparser.parse(url)
            f.write(f"<h2 class='text-xl font-semibold mt-6'>{feed.feed.get('title', 'Feed')}</h2><ul class='list-disc ml-6 mb-4'>")
            for entry in feed.entries[:3]:
                f.write(f"<li><a href='{entry.link}' class='text-blue-600 hover:underline'>{entry.title}</a> - {entry.published}</li>")
            f.write("</ul>")

        f.write(f"<p class='text-sm text-gray-500 mt-10'>Last updated: {datetime.utcnow().isoformat()} UTC</p>")
        f.write("</body></html>")

if __name__ == "__main__":
    while True:
        print("Fetching and saving latest RSS...")
        fetch_and_save()
        time.sleep(1)
