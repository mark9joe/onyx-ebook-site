import os
from datetime import datetime

# Set up output folder
PAGES_DIR = "pages"
os.makedirs(PAGES_DIR, exist_ok=True)

# Load locations and topics
with open("locations.txt", "r") as f:
    locations = [line.strip().lower().replace(",", "").replace(" ", "") for line in f if line.strip()]

with open("topics.txt", "r") as f:
    topics = [line.strip().lower().replace(" ", "") for line in f if line.strip()]

# Limit the number of pages generated for demo
MAX_PAGES = 1_000_000  # 1 trillion is impractical for any real deployment

# Initialize sitemap entries
sitemap_entries = []

count = 0
for location in locations:
    for topic in topics:
        if count >= MAX_PAGES:
            break

        filename = f"{topic}_{location}.html"
        filepath = os.path.join(PAGES_DIR, filename)
        page_url = f"https://www.respirework.com/pages/{filename}"

        html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{topic.replace('-', ' ').title()} in {location.title()} | RespireWork</title>
    <meta name=\"description\" content=\"Explore trending insights about {topic} in {location}. Stay informed via RespireWork.\">
    <meta name=\"robots\" content=\"index, follow\">
    <meta property=\"og:url\" content=\"{page_url}\"/>
    <meta http-equiv=\"refresh\" content=\"0;url=https://www.respirework.com\" />
</head>
<body>
    <p>Redirecting to <a href=\"https://www.respirework.com\">RespireWork</a>...</p>
</body>
</html>"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        sitemap_entries.append(f"<url><loc>{page_url}</loc><lastmod>{datetime.utcnow().date()}</lastmod></url>")
        count += 1

# Write sitemap.xml
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
    f.write("\n".join(sitemap_entries))
    f.write("\n</urlset>")

print(f"✅ Generated {count} pages and sitemap.xml")
