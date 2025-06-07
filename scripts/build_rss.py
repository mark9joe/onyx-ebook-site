import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree

NEWS_DIR = "news"
RSS_FILE = "rss.xml"
SITE_URL = "https://respirework.com"

def generate_rss():
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")

    SubElement(channel, "title").text = "RespireWork News Feed"
    SubElement(channel, "link").text = SITE_URL
    SubElement(channel, "description").text = "Latest news and updates"

    for filename in os.listdir(NEWS_DIR):
        if filename.endswith(".html"):
            title = filename.replace("-", " ").replace(".html", "").title()
            link = f"{SITE_URL}/news/{filename}"
            pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

            item = SubElement(channel, "item")
            SubElement(item, "title").text = title
            SubElement(item, "link").text = link
            SubElement(item, "guid").text = link
            SubElement(item, "pubDate").text = pub_date

    tree = ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)
    print(f"✅ RSS feed generated: {RSS_FILE}")

if __name__ == "__main__":
    generate_rss()
