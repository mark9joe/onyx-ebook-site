import os
from datetime import datetime
from urllib.parse import quote

# Load locations and topics
with open("locations.txt", "r") as f:
    locations = [line.strip() for line in f if line.strip()]

with open("topics.txt", "r") as f:
    topics = [line.strip() for line in f if line.strip()]

# Directory to save generated HTML files
output_dir = "pages"
os.makedirs(output_dir, exist_ok=True)

# Store sitemap entries
sitemap_entries = []

# Homepage URL
base_url = "https://www.respirework.com"

for location in locations:
    for topic in topics:
        safe_location = location.lower().replace(",", "").replace(" ", "_")
        safe_topic = topic.lower().replace(" ", "_")
        filename = f"{safe_topic}_{safe_location}.html"
        filepath = os.path.join(output_dir, filename)
        full_url = f"{base_url}/{filename}"

        # Create redirect HTML content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{topic.title()} in {location.title()} - RespireWork</title>
  <meta name="description" content="Explore trending {topic} topics in {location}. Discover insights, trends, and more. Powered by RespireWork.">
  <meta name="robots" content="index, follow">
  <meta http-equiv="refresh" content="0; url={base_url}" />
  <link rel="canonical" href="{base_url}" />
</head>
<body>
  <p>Redirecting to <a href="{base_url}">{base_url}</a>...</p>
</body>
</html>""")

        # Add entry to sitemap
        sitemap_entries.append(f"""  <url>
    <loc>{full_url}</loc>
    <lastmod>{datetime.utcnow().date()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>""")

# Write sitemap.xml
with open(os.path.join(output_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n""")
    f.write("\n".join(sitemap_entries))
    f.write("\n</urlset>")

# Print sitemap ping URLs
sitemap_url = f"{base_url}/sitemap.xml"
print("\nSubmit your sitemap to search engines:")
print("Google:", f"https://www.google.com/ping?sitemap={quote(sitemap_url)}")
print("Bing:  ", f"https://www.bing.com/ping?sitemap={quote(sitemap_url)}")
