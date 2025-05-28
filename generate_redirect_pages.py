import os
import random
from datetime import datetime
import requests

BASE_URL = "https://www.respirework.com"
PAGES_DIR = "pages"
SITEMAP_FILE = "sitemap.xml"
TOPIC_FILE = "topics.txt"
LOCATION_FILE = "locations.txt"

os.makedirs(PAGES_DIR, exist_ok=True)

def load_lines(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

def slugify(text):
    return text.lower().replace(" ", "").replace(",", "")

def generate_html(topic, location):
    filename = f"{slugify(topic)}_{slugify(location)}.html"
    filepath = os.path.join(PAGES_DIR, filename)
    url = f"{BASE_URL}/{PAGES_DIR}/{filename}"

    title = f"{topic.title()} News in {location.title()} - RespireWork"
    description = f"Trending {topic} stories from {location}. Stay updated via RespireWork."

    html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"robots\" content=\"index, follow\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{title}</title>
  <meta name=\"description\" content=\"{description}\">
  <meta http-equiv=\"refresh\" content=\"0;url={BASE_URL}\">
</head>
<body>
  <p>Redirecting to <a href=\"{BASE_URL}\">{BASE_URL}</a></p>
</body>
</html>"""

    with open(filepath, "w") as f:
        f.write(html_content)

    return url

def update_sitemap(pages):
    timestamp = datetime.utcnow().isoformat() + "Z"
    urls = "\n".join(
        f"<url><loc>{page}</loc><lastmod>{timestamp}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>"
        for page in pages
    )
    sitemap_content = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
{urls}
</urlset>"""

    with open(SITEMAP_FILE, "w") as f:
        f.write(sitemap_content)

def ping_search_engines():
    sitemap_url = f"{BASE_URL}/{SITEMAP_FILE}"
    try:
        requests.get(f"https://www.google.com/ping?sitemap={sitemap_url}")
        requests.get(f"https://www.bing.com/ping?sitemap={sitemap_url}")
        print("✅ Pinged Google and Bing.")
    except Exception as e:
        print("⚠️ Error pinging search engines:", e)

def main():
    topics = load_lines(TOPIC_FILE)
    locations = load_lines(LOCATION_FILE)
    pages = []

    for topic in topics:
        for location in random.sample(locations, min(3, len(locations))):
            url = generate_html(topic, location)
            pages.append(url)

    update_sitemap(pages)
    ping_search_engines()
    print(f"✅ {len(pages)} pages generated and indexed in sitemap.")

if __name__ == "__main__":
    main()
    
