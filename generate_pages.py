import os
from itertools import product
from datetime import datetime

# Load topics and locations
with open("topics.txt", "r", encoding="utf-8") as f:
    topics = [line.strip() for line in f if line.strip()]

with open("locations.txt", "r", encoding="utf-8") as f:
    locations = [line.strip() for line in f if line.strip()]

os.makedirs("pages", exist_ok=True)

sitemap_entries = []
rss_items = []

for topic, location in product(topics, locations):
    slug = f"{topic}_{location}".replace(" ", "_").lower()
    filename = f"{slug}.html"
    filepath = os.path.join("pages", filename)
    page_url = f"https://www.respirework.com/pages/{filename}"
    title = f"{topic.title()} News in {location.replace('_', ' ').title()}"

    html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta http-equiv=\"refresh\" content=\"0;url=https://www.respirework.com\" />
  <link rel=\"canonical\" href=\"https://www.respirework.com\" />
  <meta name=\"description\" content=\"Explore {title} and stay informed.\" />
  <meta name=\"robots\" content=\"index, follow\" />
  <title>{title} - RespireWork</title>
</head>
<body>
  <p>If you are not redirected, <a href=\"https://www.respirework.com\">click here</a>.</p>
</body>
</html>
"""

    # Write HTML
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Sitemap entry
    sitemap_entries.append(f"<url><loc>{page_url}</loc><lastmod>{datetime.utcnow().date()}</lastmod></url>")

    # RSS entry
    rss_items.append(f"""
<item>
  <title>{title}</title>
  <link>{page_url}</link>
  <description>Auto-generated page about {title}</description>
  <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
</item>
""")

# Write sitemap
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
    f.write("".join(sitemap_entries))
    f.write("\n</urlset>")

# Write RSS feed
with open("rss.xml", "w", encoding="utf-8") as f:
    f.write("""<?xml version=\"1.0\"?>
<rss version=\"2.0\">
<channel>
  <title>RespireWork Auto Pages</title>
  <link>https://www.respirework.com</link>
  <description>SEO feed of all generated pages.</description>
""")
    f.write("".join(rss_items))
    f.write("\n</channel>\n</rss>")

print("✅ Pages, sitemap.xml, and rss.xml generated successfully.")
