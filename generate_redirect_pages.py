import os
from datetime import datetime, timezone

# Config
LOCATIONS_FILE = "locations.txt"  # format: Country,City per line
TOPICS_FILE = "topics.txt"        # one topic per line, e.g. google, facebook, youtube
OUTPUT_DIR = "redirect_pages"     # output folder
REDIRECT_URL = "https://www.respirework.com"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load locations
locations = []
with open(LOCATIONS_FILE, "r", encoding="utf-8") as loc_file:
    for line in loc_file:
        line = line.strip()
        if not line or "," not in line:
            continue
        country, city = [p.strip() for p in line.split(",", 1)]
        locations.append((country, city))

# Load topics
topics = []
with open(TOPICS_FILE, "r", encoding="utf-8") as topics_file:
    for line in topics_file:
        topic = line.strip().lower()
        if topic:
            topics.append(topic)

# Current UTC date for logs (optional)
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

count = 0
for country, city in locations:
    safe_country = country.lower().replace(" ", "_")
    safe_city = city.lower().replace(" ", "_")
    for topic in topics:
        filename = f"{topic}_{safe_country}_{safe_city}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        # Redirect HTML content
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="0; url={REDIRECT_URL}" />
  <title>Redirecting to Respirework</title>
  <link rel="canonical" href="{REDIRECT_URL}" />
  <meta name="robots" content="noindex, follow" />
</head>
<body>
  <p>Redirecting to <a href="{REDIRECT_URL}">{REDIRECT_URL}</a>...</p>
</body>
</html>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Created redirect page: {filepath}")
        count += 1

print(f"\n✅ Done. Total redirect pages created: {count}")
