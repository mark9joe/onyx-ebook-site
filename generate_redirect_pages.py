import os
from datetime import datetime

# File paths
locations_file = "locations.txt"
topics_file = "topics.txt"
pages_dir = "pages"
sitemap_file = "sitemap.xml"

# Base site URL
base_url = "https://www.respirework.com"

# Ensure output directory exists
os.makedirs(pages_dir, exist_ok=True)

# Load locations and topics
with open(locations_file, "r") as f:
    locations = [line.strip().replace(",", "_").replace(" ", "_").lower() for line in f if line.strip()]

with open(topics_file, "r") as f:
    topics = [line.strip().replace(",", "_").replace(" ", "_").lower() for line in f if line.strip()]

# Page generation
generated_pages = []
for location in locations:
    for topic in topics:
        slug = f"{topic}_{location}"
        page_filename = f"{pages_dir}/{slug}.html"
        page_url = f"{base_url}/{slug}.html"

        # HTML redirect content
        html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{topic.replace('_', ' ').title()} - {location.replace('_', ' ').title()}</title>
    <meta name=\"description\" content=\"Latest updates on {topic.replace('_', ' ')} in {location.replace('_', ' ')}. Stay informed with RespireWork.\">
    <meta http-equiv=\"refresh\" content=\"0; url={base_url}\" />
</head>
<body>
    <p>Redirecting to <a href=\"{base_url}\">{base_url}</a>...</p>
</body>
</html>"""

        with open(page_filename, "w") as f:
            f.write(html_content)
            generated_pages.append(f"{page_url}")

# Update sitemap
sitemap_entries = "\n".join([f"  <url><loc>{url}</loc><lastmod>{datetime.utcnow().date()}</lastmod><changefreq>weekly</changefreq><priority>0.5</priority></url>" for url in generated_pages])
sitemap_content = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
{sitemap_entries}
</urlset>"""

with open(sitemap_file, "w") as f:
    f.write(sitemap_content)

print(f"Generated {len(generated_pages)} pages and updated sitemap.xml")

# Optional RSS Ping (print ping URLs for manual or automated use)
for url in generated_pages:
    print(f"Ping this: https://www.google.com/ping?sitemap={base_url}/sitemap.xml")
    
