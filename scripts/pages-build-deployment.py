import os
import requests
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

NEWS_DIR = "news"
BASE_URL = "https://respirework.com/news"

# Replace with your ad code
AD_CODE = """<script>
(function(wgg){
var d = document,
    s = d.createElement('script'),
    l = d.scripts[d.scripts.length - 1];
s.settings = wgg || {};
s.src = "//complete-drink.com/bgXEV/sXd.GAl/0tY/W/cW/ueomD9fuzZuU-lzkfPfT/Yo0vMGDgAexkO/DKIethNbj-QawTMADPED4WMmwo";
s.async = true;
s.referrerPolicy = 'no-referrer-when-downgrade';
l.parentNode.insertBefore(s, l);
})({})
</script>"""

TEMPLATE = """<!doctype html>
<html ⚡>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="canonical" href="{url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{visibility:hidden}}</style>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
</head>
<body>
  <h1>{title}</h1>
  <p><em>{date}</em></p>
  <p>{summary}</p>
  {ad_code}
</body>
</html>"""

def fetch_trending():
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    r = requests.get(url)
    topics = []
    if r.ok:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(r.content)
        for item in root.findall(".//item"):
            title = item.findtext("title")
            summary = item.findtext("description")
            slug = "-".join(title.lower().split())
            topics.append((title, summary, slug))
    return topics[:50]

def generate_pages(topics):
    os.makedirs(NEWS_DIR, exist_ok=True)
    for title, summary, slug in topics:
        date = datetime.utcnow().strftime("%Y-%m-%d")
        url = f"{BASE_URL}/{slug}.html"
        html = TEMPLATE.format(title=title, summary=summary, slug=slug, date=date, ad_code=AD_CODE, url=url)
        with open(os.path.join(NEWS_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(html)

def generate_rss(topics):
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = "RespireWork News Feed"
    SubElement(channel, "link").text = BASE_URL
    SubElement(channel, "description").text = "Daily trending AMP news."

    for title, summary, slug in topics:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = title
        SubElement(item, "description").text = summary
        SubElement(item, "link").text = f"{BASE_URL}/{slug}.html"

    xml_str = xml.dom.minidom.parseString(tostring(rss)).toprettyxml()
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)

def generate_sitemap(topics):
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for _, _, slug in topics:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = f"{BASE_URL}/{slug}.html"
        SubElement(url, "lastmod").text = datetime.utcnow().strftime("%Y-%m-%d")

    xml_str = xml.dom.minidom.parseString(tostring(urlset)).toprettyxml()
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)

if __name__ == "__main__":
    print("📥 Fetching trending topics...")
    topics = fetch_trending()
    print(f"✅ {len(topics)} topics found.")
    generate_pages(topics)
    generate_rss(topics)
    generate_sitemap(topics)
    print("🚀 News, RSS, and Sitemap generated.")
