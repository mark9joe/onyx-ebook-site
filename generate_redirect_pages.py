import os
import time
from datetime import datetime

# File paths
LOCATIONS_FILE = "locations.txt"
TOPICS_FILE = "topics.txt"
OUTPUT_DIR = "generated_pages"
SITEMAP_FILE = "sitemap.xml"
RSS_FILE = "feed.xml"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_locations():
    with open(LOCATIONS_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def get_topics():
    with open(TOPICS_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def generate_content(topic, location):
    # Static placeholder content generation
    return {
        "title": f"Latest {topic.title()} Trends in {location.title()}",
        "description": f"Discover the most recent updates on {topic} in {location}.",
        "body": f"<p>Stay informed with trending {topic.lower()} news and events in {location}.</p>"
    }

def write_html_file(filename, title, description, body):
    full_path = os.path.join(OUTPUT_DIR, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <meta name=\"description\" content=\"{description}\">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    {body}
    <hr>
    <p>Visit our homepage: <a href=\"https://www.respirework.com\">https://www.respirework.com</a></p>
</body>
</html>
        ")
    print(f"Created page: https://www.respirework.com/{filename}")
    return filename

def generate_sitemap(urls):
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write("""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
""")
        for url in urls:
            f.write(f"  <url>\n    <loc>https://www.respirework.com/{url}</loc>\n    <lastmod>{datetime.utcnow().isoformat()}Z</lastmod>\n  </url>\n")
        f.write("</urlset>")
    print("✅ Sitemap generated")

def generate_rss(urls):
    with open(RSS_FILE, "w", encoding="utf-8") as f:
        f.write("""<?xml version=\"1.0\" encoding=\"UTF-8\" ?>
<rss version=\"2.0\">
<channel>
  <title>RespireWork AI Content</title>
  <link>https://www.respirework.com</link>
  <description>AI generated content by location and topic</description>
""")
        for url in urls:
            f.write(f"  <item>\n    <title>{url.replace('.html','')}</title>\n    <link>https://www.respirework.com/{url}</link>\n    <guid>https://www.respirework.com/{url}</guid>\n    <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>\n  </item>\n")
        f.write("</channel>\n</rss>")
    print("✅ RSS feed generated")

def main():
    locations = get_locations()
    topics = get_topics()
    generated_urls = []

    for location in locations:
        for topic in topics:
            filename = f"{topic.lower().replace(' ','_')}_{location.lower().replace(',','').replace(' ','_')}.html"
            content = generate_content(topic, location)
            write_html_file(filename, content["title"], content["description"], content["body"])
            generated_urls.append(filename)
            time.sleep(1)  # Be polite

    generate_sitemap(generated_urls)
    generate_rss(generated_urls)

if __name__ == "__main__":
    main()
    
