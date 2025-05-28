import os
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
import urllib.parse
import urllib.request

# Configuration
output_dir = "generated_pages"
site_url = "https://www.respirework.com"
os.makedirs(output_dir, exist_ok=True)

# Load topics and locations
with open("locations.txt", "r", encoding="utf-8") as f:
    locations = [line.strip() for line in f if line.strip()]

with open("topics.txt", "r", encoding="utf-8") as f:
    topics = [line.strip() for line in f if line.strip()]

# Page generation
for location in locations:
    for topic in topics:
        filename = f"{topic.lower()}_{location.lower().replace(',', '').replace(' ', '_')}.html"
        filepath = os.path.join(output_dir, filename)

        title = f"{topic.title()} News in {location.title()} - RespireWork"
        description = f"Explore trending {topic} news and insights from {location}, powered by AI."

        content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="{description}">
            <meta name="robots" content="index, follow">
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            <p>{description}</p>
            <p>Visit our homepage for more: <a href="{site_url}">{site_url}</a></p>
        </body>
        </html>
        """

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created page: {site_url}/{filename}")

# Generate sitemap.xml
sitemap_root = Element("urlset")
sitemap_root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

for file in os.listdir(output_dir):
    if file.endswith(".html"):
        url = SubElement(sitemap_root, "url")
        loc = SubElement(url, "loc")
        loc.text = f"{site_url}/{file}"
        lastmod = SubElement(url, "lastmod")
        lastmod.text = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

sitemap_str = xml.dom.minidom.parseString(tostring(sitemap_root)).toprettyxml(indent="  ")
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_str)
print("🗺️ Sitemap generated: sitemap.xml")

# Ping search engines
sitemap_url = f"{site_url}/sitemap.xml"
ping_urls = [
    f"http://www.google.com/ping?sitemap={urllib.parse.quote(sitemap_url)}",
    f"http://www.bing.com/ping?sitemap={urllib.parse.quote(sitemap_url)}"
]

for url in ping_urls:
    try:
        response = urllib.request.urlopen(url)
        print(f"📡 Pinged: {url} (Status: {response.status})")
    except Exception as e:
        print(f"❌ Error pinging {url}: {e}")
        
