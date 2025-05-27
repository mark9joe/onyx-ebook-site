import os
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

LOCATIONS_FILE = "locations.txt"
TOPICS_FILE = "topics.txt"
OUTPUT_DIR = "generated_pages"
BASE_URL = "https://www.respirework.com"

# Create output dir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read locations
locations = []
with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) == 2:
            country, city = parts
            locations.append((country.strip(), city.strip()))

# Read topics
topics = []
with open(TOPICS_FILE, "r", encoding="utf-8") as f:
    for line in f:
        topic = line.strip()
        if topic:
            topics.append(topic)

print(f"Loaded {len(locations)} locations and {len(topics)} topics.")

# Generate redirect HTML
def generate_redirect_html(target_url):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="0; url={target_url}" />
  <link rel="canonical" href="{target_url}" />
  <title>Redirecting...</title>
</head>
<body>
  <p>If you are not redirected automatically, follow this <a href="{target_url}">link</a>.</p>
</body>
</html>"""

urls_for_sitemap = []

for country, city in locations:
    safe_country = country.lower().replace(" ", "_")
    safe_city = city.lower().replace(" ", "_")
    for topic in topics:
        safe_topic = topic.lower().replace(" ", "_")
        filename = f"{safe_country}_{safe_city}_{safe_topic}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        # Each page redirects to BASE_URL homepage
        html_content = generate_redirect_html(BASE_URL)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        full_url = f"{BASE_URL}/{filename}"
        urls_for_sitemap.append(full_url)
        print(f"Created redirect page: {full_url}")

# Generate sitemap.xml
urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

for url in urls_for_sitemap:
    url_el = SubElement(urlset, "url")
    loc_el = SubElement(url_el, "loc")
    loc_el.text = url
    lastmod_el = SubElement(url_el, "lastmod")
    lastmod_el.text = now_iso

# Prettify XML
raw_xml = tostring(urlset, 'utf-8')
pretty_xml = parseString(raw_xml).toprettyxml(indent="  ")

with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(pretty_xml)

print(f"Sitemap generated with {len(urls_for_sitemap)} URLs.")
