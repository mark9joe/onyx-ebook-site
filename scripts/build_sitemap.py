import os
from datetime import datetime

NEWS_DIR = "news"
SITEMAP_FILE = "sitemap.xml"
SITE_URL = "https://respirework.com"

def generate_sitemap():
    urls = []
    for filename in os.listdir(NEWS_DIR):
        if filename.endswith(".html"):
            url = f"{SITE_URL}/news/{filename}"
            urls.append(url)

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in urls:
            f.write("  <url>\n")
            f.write(f"    <loc>{url}</loc>\n")
            f.write(f"    <lastmod>{datetime.utcnow().date()}</lastmod>\n")
            f.write("    <changefreq>hourly</changefreq>\n")
            f.write("    <priority>0.8</priority>\n")
            f.write("  </url>\n")
        f.write("</urlset>\n")

    print(f"✅ Sitemap generated: {SITEMAP_FILE}")

if __name__ == "__main__":
    generate_sitemap()
