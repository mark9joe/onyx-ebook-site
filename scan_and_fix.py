import os
from urllib.parse import urlparse
from generate_template import generate_html
from datetime import datetime

broken_urls = [
    "events/yarros-tour-2025",
    "news/fourth-wing-award",
    "hundreds-of-millions-at-risk-from-chinese-shopping-app-malware",
    "ukraines-zelensky-regrets-meltdown-meeting-with-trump-and-vows-to-work-together-for-peace"
]

sitemap_path = "sitemap.xml"
domain = "https://www.respirework.com"

def create_page(path):
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(f"{path}/index.html", "w") as f:
        f.write(generate_html(title=path.replace("-", " ").title()))

def update_sitemap(pages):
    if not os.path.exists(sitemap_path):
        with open(sitemap_path, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    with open(sitemap_path, "a") as f:
        for page in pages:
            f.write("  <url>\n")
            f.write(f"    <loc>{domain}/{page}</loc>\n")
            f.write(f"    <lastmod>{datetime.utcnow().strftime('%Y-%m-%d')}</lastmod>\n")
            f.write("    <changefreq>weekly</changefreq>\n")
            f.write("    <priority>0.8</priority>\n")
            f.write("  </url>\n")

    with open(sitemap_path, "a") as f:
        f.write('</urlset>\n')

if __name__ == "__main__":
    fixed = []
    for url in broken_urls:
        if not os.path.exists(os.path.join(url, "index.html")):
            create_page(url)
            fixed.append(url)
    if fixed:
        update_sitemap(fixed)
        print(f"Fixed and added to sitemap: {fixed}")
    else:
        print("No missing pages found.")
