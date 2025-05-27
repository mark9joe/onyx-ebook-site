import os
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Configuration
OUTPUT_DIR = "redirect_pages"
LOCATIONS_FILE = "locations.txt"
REDIRECT_URL = "https://www.respirework.com"
SITEMAP_FILE = "sitemap.xml"
MODEL = "gpt-3.5-turbo"

# Init OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load locations
with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
    locations = [line.strip() for line in f if line.strip()]

# Generate pages and sitemap
sitemap_entries = []
today = datetime.utcnow().strftime("%Y-%m-%d")

for entry in locations:
    parts = entry.split(',')
    if len(parts) != 2:
        print(f"Skipping invalid line: {entry}")
        continue

    country = parts[0].strip().lower().replace(" ", "_")
    city = parts[1].strip().lower().replace(" ", "_")
    filename = f"{country}_{city}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        # Fetch SEO content
        prompt = f"Write a short trending news-style SEO paragraph for {city.title()}, {country.title()}. End with a call to action to visit Respirework."
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error fetching content for {entry}: {e}")
        content = f"<p>Explore {city.title()}, {country.title()} - Visit our homepage <a href=\"{REDIRECT_URL}\">here</a>.</p>"

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <meta http-equiv=\"refresh\" content=\"0; url={REDIRECT_URL}\">
  <title>{city.title()}, {country.title()} - Redirecting...</title>
</head>
<body>
  {content}
  <p><a href=\"{REDIRECT_URL}\">Click here if you're not redirected</a>.</p>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    sitemap_entries.append(f"<url><loc>{REDIRECT_URL}/{filename}</loc><lastmod>{today}</lastmod></url>")
    print(f"✅ Created: {REDIRECT_URL}/{filename}")

# Generate sitemap
sitemap_path = os.path.join(OUTPUT_DIR, SITEMAP_FILE)
sitemap_xml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
{''.join(sitemap_entries)}
</urlset>"""

with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print(f"\n✅ Sitemap generated at: {sitemap_path}")
