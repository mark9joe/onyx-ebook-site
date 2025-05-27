import os
import openai
from datetime import datetime

# Load OpenAI Key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create output directory if it doesn't exist
OUTPUT_DIR = "."
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://www.respirework.com"

def load_list(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

locations = load_list("locations.txt")  # Format: country,city
topics = load_list("topics.txt")        # Format: one topic per line

urls = []

for loc in locations:
    country, city = map(str.strip, loc.split(","))
    for topic in topics:
        slug = f"{topic.lower()}_{country.lower()}_{city.lower().replace(' ', '_')}"
        filename = f"{slug}.html"
        path = os.path.join(OUTPUT_DIR, filename)

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f"Write 3 SEO paragraphs about '{topic}' in {city}, {country}. End with a CTA to visit https://www.respirework.com."
                }],
                max_tokens=500
            )
            content = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Error fetching content for {country},{city}: {e}")
            continue

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{topic.title()} in {city}, {country}</title>
  <meta name="description" content="Discover {topic} updates from {city}, {country}.">
  <meta http-equiv="refresh" content="5; URL={BASE_URL}">
</head>
<body>
  <h1>{topic.title()} in {city}, {country}</h1>
  <p>{content}</p>
  <p>Redirecting to <a href="{BASE_URL}">{BASE_URL}</a>...</p>
</body>
</html>"""

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        urls.append(f"{BASE_URL}/{filename}")
        print(f"✅ Created page: {BASE_URL}/{filename}")

# Update sitemap.xml
with open(SITEMAP_FILE, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for url in urls:
        f.write(f"<url><loc>{url}</loc><lastmod>{datetime.utcnow().date()}</lastmod></url>\n")
    f.write('</urlset>\n')

print("✅ Sitemap updated.")
