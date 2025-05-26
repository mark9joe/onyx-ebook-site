from datetime import datetime

def build_rss(feed_title, feed_link, feed_description, items):
    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>{feed_title}</title>
  <link>{feed_link}</link>
  <description>{feed_description}</description>
"""
    for item in items:
        rss += f"""  <item>
    <title>{item['title']}</title>
    <link>{item['link']}</link>
    <description>{item['description']}</description>
    <pubDate>{item['pubDate']}</pubDate>
    <guid isPermaLink="false">{item['guid']}</guid>
  </item>
"""
    rss += "</channel>\n</rss>"
    return rss


def write_feed(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


now = datetime.utcnow()
timestamp = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

# Sample items
items = [{
    "title": "New Chapter Released: Storm of Shadows",
    "link": "https://www.respirework.com/empyrean",
    "description": "The latest release from the Empyrean series is now available.",
    "pubDate": timestamp,
    "guid": f"empyrean-{int(now.timestamp())}"
}]

# Main RSS Feed
main_feed = build_rss("Respirework Feed", "https://www.respirework.com", "Main website feed", items)
write_feed("rss.xml", main_feed)

# Empyrean Series Feed
empyrean_feed = build_rss("The Empyrean Series", "https://www.respirework.com/empyrean", "News and updates from the fantasy book series", items)
write_feed("empyrean-series.xml", empyrean_feed)

# Rebecca Yarros Feed
yarros_items = [{
    "title": "Onyx Storm: Launch Announcement",
    "link": "https://www.respirework.com/rebecca-yarros",
    "description": "Rebecca Yarros' newest fantasy ebook is live now.",
    "pubDate": timestamp,
    "guid": f"yarros-{int(now.timestamp())}"
}]
yarros_feed = build_rss("Rebecca Yarros News", "https://www.respirework.com/rebecca-yarros", "Author announcements and events", yarros_items)
write_feed("rebecca-yarros.xml", yarros_feed)

print("✅ RSS feeds generated.")
