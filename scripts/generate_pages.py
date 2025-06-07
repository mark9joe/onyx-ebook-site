File: scripts/generate_pages.py

import os import requests from datetime import datetime from xml.etree import ElementTree as ET

NEWS_DIR = "news" TOPIC_SOURCE = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US" TEMPLATE = ''' <!doctype html>

<html amp lang="en">
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <link rel="canonical" href="https://www.respirework.com/news/{slug}.html">
    <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
    <meta name="description" content="{summary}">
    <script async src="https://cdn.ampproject.org/v0.js"></script>
    <style amp-boilerplate>body{visibility:hidden}</style>
  </head>
  <body>
    <h1>{title}</h1>
    <p><em>{date}</em></p>
    <p>{summary}</p>
    {ads}
  </body>
</html>
'''ADS_BLOCK = '''<script> (function(wgg){ var d = document, s = d.createElement('script'), l = d.scripts[d.scripts.length - 1]; s.settings = wgg || {}; s.src = "//complete-drink.com/bgXEV/sXd.GAl/0tY/W/cW/ueomD9fuzZuU-lzkfPfT/Yo0vMGDgAexkO/DKIethNbj-QawTMADPED4WMmwo"; s.async = true; s.referrerPolicy = 'no-referrer-when-downgrade'; l.parentNode.insertBefore(s, l); })({}) </script>'''

def fetch_trending_topics(): response = requests.get(TOPIC_SOURCE) items = [] if response.ok: root = ET.fromstring(response.content) for item in root.findall(".//item"): title = item.findtext("title") summary = item.findtext("description") slug = "-".join(title.lower().split()) items.append((title, summary, slug)) return items[:100]

def save_page(title, summary, slug): date = datetime.utcnow().strftime("%Y-%m-%d") html = TEMPLATE.format(title=title, summary=summary, slug=slug, date=date, ads=ADS_BLOCK) path = os.path.join(NEWS_DIR, f"{slug}.html") with open(path, "w", encoding="utf-8") as f: f.write(html)

if name == "main": os.makedirs(NEWS_DIR, exist_ok=True) topics = fetch_trending_topics() for title, summary, slug in topics: save_page(title, summary, slug) print(f"Generated {len(topics)} AMP news pages.")
