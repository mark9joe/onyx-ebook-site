import os
import time
from datetime import datetime

# Configuration
output_dir = "pages"
homepage_url = "https://www.respirework.com"
location_file = "locations.txt"
topic_file = "topics.txt"
sitemap_file = "sitemap.xml"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load locations and topics
with open(location_file, 'r') as f:
    locations = [line.strip().replace(",", "_").replace(" ", "_").lower() for line in f.readlines() if line.strip()]

with open(topic_file, 'r') as f:
    topics = [line.strip().replace(" ", "_").lower() for line in f.readlines() if line.strip()]

# Create a sitemap header
sitemap_entries = [
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
    "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
]

# Generate pages
count = 0
for location in locations:
    for topic in topics:
        if count >= 100000:
            break
        filename = f"{topic}_{location}.html"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <meta name=\"description\" content=\"Latest updates and trends on {topic.replace('_', ' ')} in {location.replace('_', ' ').title()}.\">
    <meta name=\"robots\" content=\"index, follow\">
    <meta http-equiv=\"refresh\" content=\"0; url={homepage_url}\">
    <title>{topic.replace('_', ' ').title()} in {location.replace('_', ' ').title()}</title>
</head>
<body>
    <p>If you're not redirected automatically, visit <a href=\"{homepage_url}\">our homepage</a>.</p>
</body>
</html>
""")

        sitemap_entries.append(f"  <url><loc>{homepage_url}/pages/{filename}</loc><lastmod>{datetime.utcnow().date()}</lastmod></url>")
        count += 1

# Close sitemap
sitemap_entries.append("</urlset>")

# Write sitemap.xml
with open(sitemap_file, 'w') as f:
    f.write("\n".join(sitemap_entries))

print(f"✅ Generated {count} pages and sitemap.xml")

# Optionally: ping search engines (basic method)
import requests
for engine in [
    f"http://www.google.com/ping?sitemap={homepage_url}/sitemap.xml",
    f"http://www.bing.com/ping?sitemap={homepage_url}/sitemap.xml"
]:
    try:
        res = requests.get(engine)
        print(f"Pinged {engine}: {res.status_code}")
    except Exception as e:
        print(f"Failed to ping {engine}: {e}")
            
