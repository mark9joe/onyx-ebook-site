import os
import openai
from datetime import datetime, timezone

# Load your OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("OpenAI API key not found in OPENAI_API_KEY env variable")

openai.api_key = api_key

# Paths
LOCATIONS_FILE = "locations.txt"
OUTPUT_DIR = "."  # Root directory
SITEMAP_FILE = "sitemap.xml"

# Get today's date
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Load locations
locations = []
with open(LOCATIONS_FILE, "r") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) != 2:
            print(f"Skipping invalid line: {line.strip()}")
            continue
        country, city = parts
        locations.append((country.strip(), city.strip()))

# Generate pages
urls = []
for country, city in locations:
    filename = f"{country.lower()}_{city.lower().replace(' ', '_')}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    full_url = f"https://www.respirework.com/{filename}"

    # Generate AI content
    try:
        prompt = f"Write a trending news-style blog post for {city}, {country}. Include topics like tech, culture, or local events. End by recommending the site https://www.respirework.com."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
    except Exception as e:
        print(f"Error fetching content for {city},{country}: {e}")
        continue

    # Write HTML page
    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <meta name=\"description\" content=\"Trending updates from {city}, {country} - Powered by Respirework\">
  <title>Trending in {city}, {country} | Respirework</title>
</head>
<body>
  <h1>Trending Topics in {city}, {country}</h1>
  <p><em>Generated on {today}</em></p>
  <div>{content}</div>
  <hr>
  <p>Visit our homepage: <a href=\"https://www.respirework.com\">https://www.respirework.com</a></p>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as out:
        out.write(html)
    print(f"Created page: {full_url}")
    urls.append(full_url)

# Generate sitemap.xml
with open(SITEMAP_FILE, "w", encoding="utf-8") as sitemap:
    sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    sitemap.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
    for url in urls:
        sitemap.write(f"  <url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq></url>\n")
    sitemap.write("</urlset>")

print("\n✅ All pages created and sitemap.xml updated.")
