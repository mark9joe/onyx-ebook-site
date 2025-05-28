import os
from datetime import datetime
from urllib.parse import quote

# Load locations and topics
with open("locations.txt", "r") as loc_file:
    locations = [line.strip().replace(",", "_").replace(" ", "").lower() for line in loc_file.readlines()]

with open("topics.txt", "r") as topic_file:
    topics = [line.strip().replace(" ", "").lower() for line in topic_file.readlines()]

# Directory for pages
os.makedirs("pages", exist_ok=True)

# Sitemap and RSS
sitemap_entries = []
rss_items = []

# Base website URL
base_url = "https://www.respirework.com"

# Time for feed
now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

# Generate pages
count = 0
for location in locations:
    for topic in topics:
        slug = f"{topic}_{location}.html"
        page_url = f"{base_url}/pages/{slug}"

        # HTML content with redirect and metadata
        html_content = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta http-equiv=\"refresh\" content=\"0; url={base_url}\">
  <link rel=\"canonical\" href=\"{base_url}\">
  <title>{topic.title()} in {location.title()}</title>
  <meta name=\"description\" content=\"Explore trending topics about {topic.title()} in {location.title()}. Stay informed via RespireWork.\">
</head>
<body>
  <p>Redirecting to <a href=\"{base_url}\">{base_url}</a>...</p>
</body>
</html>
"""

        # Write page
        with open(f"pages/{slug}", "w") as f:
            f.write(html_content)

        # Add to sitemap
        sitemap_entries.append(f"<url><loc>{page_url}</loc><lastmod>{datetime.utcnow().date()}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>")

        # Add to RSS feed
        rss_items.append(f"""
<item>
  <title>{topic.title()} in {location.title()}</title>
  <link>{page_url}</link>
  <description>Discover {topic} news from {location}, brought to you by RespireWork.</description>
  <pubDate>{now}</pubDate>
</item>""")

        count += 1

# Write sitemap.xml
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
    f.write("""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n""")
    for url in sitemap_entries:
        f.write(f"""  <url><loc>{url}</loc></url>\n""")
    f.write("""</urlset>""")

# Write RSS feed
with open("rss.xml", "w") as f:
    f.write("""<?xml version=\"1.0\"?>
<rss version=\"2.0\">
<channel>
  <title>RespireWork RSS Feed</title>
  <link>https://www.respirework.com</link>
  <description>Latest generated content</description>
  <lastBuildDate>{now}</lastBuildDate>
""" + "\n".join(rss_items) + "\n</channel>\n</rss>")

print(f"✅ Generated {count} pages, sitemap.xml, and rss.xml")
