import os
import random
from datetime import datetime

BASE_URL = "https://www.respirework.com"
OUTPUT_DIR = "pages"
SITEMAP_FILE = "sitemap.xml"
TOPIC_FILE = "topics.txt"
LOCATION_FILE = "locations.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_lines(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def generate_html(topic, location):
    filename = f"{topic.lower()}_{location.lower().replace(',', '').replace(' ', '')}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    full_url = f"{BASE_URL}/{filename}"

    title = f"{topic.title()} News in {location.title()} - RespireWork"
    description = f"Explore trending topics about {topic} in {location}. Visit RespireWork for more."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="robots" content="index, follow">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta http-equiv="refresh" content="0;url={BASE_URL}">
</head>
<body>
  <p>Redirecting to <a href="{BASE_URL}">{BASE_URL}</a></p>
</body>
</html>"""

    with open(filepath, "w") as f:
        f.write(html)

    return filename, full_url

def update_sitemap(pages):
    timestamp = datetime.utcnow().isoformat() + "Z"
    sitemap_entries = "\n".join(
        f"""<url><loc>{url}</loc><lastmod>{timestamp}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"""
        for _, url in pages
    )
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}
</urlset>"""
    with open(SITEMAP_FILE, "w") as f:
        f.write(sitemap)

# MAIN
topics = load_lines(TOPIC_FILE)
locations = load_lines(LOCATION_FILE)
pages_created = []

for topic in topics:
    for location in random.sample(locations, min(3, len(locations))):  # Limit to 3 locations per topic
        filename, url = generate_html(topic, location)
        pages_created.append((filename, url))

update_sitemap(pages_created)

print(f"✅ Generated {len(pages_created)} pages.")
