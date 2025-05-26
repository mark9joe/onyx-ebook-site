import os
from datetime import datetime
from pathlib import Path

base_url = "https://www.respirework.com"
public_dir = Path("public")
sitemap_path = Path("public/sitemap.xml")

urls = []

# Walk through public/ directory and collect all index.html files
for root, dirs, files in os.walk(public_dir):
    for file in files:
        if file == "index.html":
            rel_path = Path(root).relative_to(public_dir)
            url = f"{base_url}/{rel_path}/".replace("\", "/")
            urls.append(url)

# Build XML sitemap content
now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in urls:
    sitemap_xml += "  <url>\n"
    sitemap_xml += f"    <loc>{url}</loc>\n"
    sitemap_xml += f"    <lastmod>{now}</lastmod>\n"
    sitemap_xml += "    <changefreq>daily</changefreq>\n"
    sitemap_xml += "    <priority>0.8</priority>\n"
    sitemap_xml += "  </url>\n"

sitemap_xml += "</urlset>\n"

# Save to sitemap.xml
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print(f"Updated sitemap with {len(urls)} entries.")
