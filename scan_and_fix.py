import os
from urllib.parse import urlparse
from generate_template import generate_template

# Directory where your static site is stored
BASE_DIR = "."

# List of broken/missing paths (relative to domain)
BROKEN_PATHS = [
    "events/yarros-tour-2025",
    "news/fourth-wing-award",
    "hundreds-of-millions-at-risk-from-chinese-shopping-app-malware",
    "ukraines-zelensky-regrets-meltdown-meeting-with-trump-and-vows-to-work-together-for-peace"
]

SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap.xml")

def generate_page(slug):
    html = generate_template(slug)
    page_dir = os.path.join(BASE_DIR, slug)
    os.makedirs(page_dir, exist_ok=True)
    file_path = os.path.join(page_dir, "index.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {file_path}")

def update_sitemap(urls):
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        sitemap += f"  <url><loc>https://www.respirework.com/{url}</loc></url>\n"

    sitemap += '</urlset>\n'

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Updated sitemap.xml with {len(urls)} entries.")

def main():
    generated_urls = []

    for slug in BROKEN_PATHS:
        index_path = os.path.join(BASE_DIR, slug, "index.html")
        if not os.path.exists(index_path):
            generate_page(slug)
            generated_urls.append(slug)

    if generated_urls:
        update_sitemap(generated_urls)
    else:
        print("No new pages generated. Sitemap not updated.")

if __name__ == "__main__":
    main()
