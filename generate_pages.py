import os
import csv
from datetime import datetime

# Paths
locations_file = "locations.csv"
output_folder = "generated_pages"
sitemap_file = os.path.join(output_folder, "sitemap.xml")

# Footer to include in every page
footer_html = """
<footer style="margin-top: 50px; font-size: 14px; text-align: center;">
  <p>&copy; 2025 Respirework. All rights reserved.</p>
  <p>
    <a href="/index.html">Home</a> | 
    <a href="/rss/empyrean-series.xml">RSS Feed</a> | 
    <a href="/privacy.html">Privacy</a> | 
    <a href="/terms.html">Terms</a> | 
    <a href="/sitemap.xml">Sitemap</a>
  </p>
</footer>
"""

# HTML Page Template
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Top Fantasy Ebooks in {{ city }}, {{ country }}</title>
  <meta name="description" content="Find the best fantasy ebooks in {{ city }}, {{ country }}. Read Onyx Storm by Rebecca Yarros.">
</head>
<body>
  <h1>Top Fantasy Ebooks in {{ city }}, {{ country }}</h1>
  <p>"Onyx Storm" is the latest epic fantasy in The Empyrean series. Buy it today!</p>
  <a href="https://www.respirework.com/onyx-storm">Buy Now</a>
  {{ footer }}
</body>
</html>
"""

# Prepare output folder
os.makedirs(output_folder, exist_ok=True)

# Read locations
with open(locations_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    locations = list(reader)

# Build sitemap
sitemap_entries = []
today = datetime.utcnow().strftime("%Y-%m-%d")

for country, city in locations:
    filename = f"top-fantasy-ebooks-in-{city.lower().replace(' ', '-')}-{country.lower().replace(' ', '-')}.html"
    filepath = os.path.join(output_folder, filename)

    # Replace placeholders
    html = html_template.replace("{{ city }}", city.title()).replace("{{ country }}", country.title())
    html = html.replace("{{ footer }}", footer_html)

    # Write page
    with open(filepath, "w", encoding="utf-8") as page:
        page.write(html)

    # Add to sitemap
    sitemap_entries.append(f"""
  <url>
    <loc>https://www.respirework.com/generated_pages/{filename}</loc>
    <lastmod>{today}</lastmod>
  </url>
""")

# Write sitemap
with open(sitemap_file, "w", encoding="utf-8") as f:
    f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(sitemap_entries)}
</urlset>
""")
