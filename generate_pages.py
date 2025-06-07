File: scripts/generate_pages.py

Purpose: Generate AMP news pages based on trending topics

import os import requests from datetime import datetime

NEWS_DIR = "news" TOPIC_SOURCE = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US" TEMPLATE = '''<!doctype html>

<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="canonical" href="https://respirework.com/news/{slug}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <meta name="description" content="{summary}">
  <style amp-boilerplate>body{visibility:hidden}</style>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
</head>
<body>
  <h1>{title}</h1>
  <p><em>{date}</em></p>
  <p>{summary}</p>
  <hr>
  <div>{ads}</div>
</body>
</html>'''ADS_BLOCK = '''<script> (function(wgg){ var d = document, s = d.createElement('script'), l = d.scripts[d.scripts.length - 1]; s.settings = wgg || {}; s.src = "//complete-drink.com/bgXEV/sXd.GAl/0tY/W/cW/ueomD9fuzZuU-lzkfPfT/Yo0vMGDgAexkO/DKIethNbj-QawTMADPED4WMmwo"; s.async = true; s.referrerPolicy = 'no-referrer-when-downgrade'; l.parentNode.insertBefore(s, l); })({}) </script>'''

def fetch_trending_topics(): response = requests.get(TOPIC_SOURCE) items = [] if response.ok: from xml.etree import ElementTree as ET root = ET.fromstring(response.content) for item in root.findall(".//item"): title = item.findtext("title") summary = item.findtext("description") slug = "-".join(title.lower().split()) items.append((title, summary, slug)) return items[:100]

def save_page(title, summary, slug): date = datetime.utcnow().strftime("%Y-%m-%d") html = TEMPLATE.format(title=title, summary=summary, slug=slug, date=date, ads=ADS_BLOCK) path = os.path.join(NEWS_DIR, f"{slug}.html") with open(path, "w", encoding="utf-8") as f: f.write(html)

if name == "main": os.makedirs(NEWS_DIR, exist_ok=True) topics = fetch_trending_topics() for title, summary, slug in topics: save_page(title, summary, slug) print(f"Generated {len(topics)} AMP news pages.")

File: scripts/build_rss.py

Purpose: Generate RSS feed from AMP news pages

import os from datetime import datetime

NEWS_DIR = "news" RSS_PATH = os.path.join("public", "rss.xml") BASE_URL = "https://respirework.com/news/"

RSS_HEADER = '''<?xml version="1.0" encoding="UTF-8"?> <rss version="2.0"> <channel>

  <title>RespireWork News</title>
  <link>https://respirework.com</link>
  <description>Trending news from RespireWork</description>
'''RSS_ITEM = '''  <item> <title>{title}</title> <link>{url}</link> <guid>{url}</guid> <pubDate>{date}</pubDate> </item> '''

RSS_FOOTER = '''</channel> </rss> '''

def generate_rss(): items = [] for file in sorted(os.listdir(NEWS_DIR)): if file.endswith(".html"): slug = file[:-5] title = slug.replace("-", " ").title() url = BASE_URL + file pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000") items.append(RSS_ITEM.format(title=title, url=url, date=pub_date))

rss = RSS_HEADER + "".join(items) + RSS_FOOTER
os.makedirs(os.path.dirname(RSS_PATH), exist_ok=True)
with open(RSS_PATH, "w", encoding="utf-8") as f:
    f.write(rss)
print(f"Generated RSS with {len(items)} items.")

if name == "main": generate_rss()

File: scripts/build_sitemap.py

Purpose: Generate sitemap.xml from AMP news pages

SITEMAP_PATH = os.path.join("public", "sitemap.xml") SITEMAP_HEADER = '''<?xml version="1.0" encoding="UTF-8"?> <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"> ''' SITEMAP_ITEM = '''  <url><loc>{url}</loc></url> ''' SITEMAP_FOOTER = '''</urlset> '''

def generate_sitemap(): items = [] for file in sorted(os.listdir(NEWS_DIR)): if file.endswith(".html"): url = BASE_URL + file items.append(SITEMAP_ITEM.format(url=url)) sitemap = SITEMAP_HEADER + "".join(items) + SITEMAP_FOOTER os.makedirs(os.path.dirname(SITEMAP_PATH), exist_ok=True) with open(SITEMAP_PATH, "w", encoding="utf-8") as f: f.write(sitemap) print(f"Generated sitemap with {len(items)} URLs.")

if name == "main": generate_sitemap()

File: public/cloak.js

// Purpose: Cloaking script to detect bots and serve alternate content

(function() { const bots = [/googlebot/i, /bingbot/i, /slurp/i, /duckduckbot/i, /baiduspider/i]; const ua = navigator.userAgent; if (bots.some(bot => bot.test(ua))) { document.write('<meta http-equiv="refresh" content="0; url=https://respirework.com">'); } })();

