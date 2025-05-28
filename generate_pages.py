import os
import hashlib
from itertools import product
from pathlib import Path
from datetime import datetime

# Constants
BASE_URL = "https://www.respirework.com"
PAGES_DIR = Path("pages")
SITEMAP_DIR = Path("sitemaps")
RSS_DIR = Path("rssfeeds")
MAX_URLS_PER_SITEMAP = 50000  # per Google guideline

# Read topics and locations
with open("topics.txt", "r", encoding="utf-8") as f:
    topics = [line.strip() for line in f if line.strip()]
with open("locations.txt", "r", encoding="utf-8") as f:
    locations = [line.strip() for line in f if line.strip()]

# Ensure directories exist
PAGES_DIR.mkdir(exist_ok=True)
SITEMAP_DIR.mkdir(exist_ok=True)
RSS_DIR.mkdir(exist_ok=True)

urls = []
rss_items = []

print("Generating HTML pages with redirection...")
for topic, location in product(topics, locations):
    slug = f"{topic}_{location}".lower().replace(" ", "-")
    filename = PAGES_DIR / f"{slug}.html"
    page_url = f"{BASE_URL}/pages/{slug}.html"

    # Write HTML page
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="0; url={BASE_URL}" />
            <title>{topic.title()} in {location.title()}</title>
            <meta name="description" content="Trending {topic} updates in {location}. Visit RespireWork." />
        </head>
        <body>
            <p>Redirecting to <a href='{BASE_URL}'>{BASE_URL}</a></p>
        </body>
        </html>
        """)
    urls.append(page_url)

    # Add to RSS items
    rss_items.append(f"""
    <item>
        <title>{topic.title()} in {location.title()}</title>
        <link>{page_url}</link>
        <description>Latest update on {topic} in {location}</description>
        <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    </item>
    """)

print("Generating RSS feeds...")
rss_chunks = [rss_items[i:i+50000] for i in range(0, len(rss_items), 50000)]
for i, chunk in enumerate(rss_chunks, start=1):
    with open(RSS_DIR / f"rss{i}.xml", "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>RespireWork RSS Feed</title>
<link>https://www.respirework.com</link>
<description>Massive updates on worldwide trending topics.</description>
        """)
        f.writelines(chunk)
        f.write("""
</channel>
</rss>
        """)

print("Generating sitemap files...")
sitemap_chunks = [urls[i:i+MAX_URLS_PER_SITEMAP] for i in range(0, len(urls), MAX_URLS_PER_SITEMAP)]
sitemap_urls = []
for i, chunk in enumerate(sitemap_chunks, start=1):
    sitemap_file = SITEMAP_DIR / f"sitemap{i}.xml"
    sitemap_url = f"{BASE_URL}/sitemaps/sitemap{i}.xml"
    sitemap_urls.append(sitemap_url)

    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        """)
        for url in chunk:
            f.write(f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{datetime.utcnow().date()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
            """)
        f.write("</urlset>")

# Create sitemap index file
with open(SITEMAP_DIR / "sitemap_index.xml", "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    """)
    for sitemap_url in sitemap_urls:
        f.write(f"""
  <sitemap>
    <loc>{sitemap_url}</loc>
    <lastmod>{datetime.utcnow().date()}</lastmod>
  </sitemap>
        """)
    f.write("</sitemapindex>")

print(f"✅ Generated {len(urls)} pages, {len(sitemap_chunks)} sitemap files, and {len(rss_chunks)} RSS files.")
