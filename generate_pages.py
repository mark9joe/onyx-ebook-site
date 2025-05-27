import os
from datetime import datetime, timezone

# Paths
LOCATIONS_FILE = "locations.txt"
OUTPUT_DIR = "."  # Root directory
SITEMAP_FILE = "sitemap.txt"

# Get today's date in UTC
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Load locations
locations = []
with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) != 2:
            print(f"⚠️ Skipping invalid line: {line.strip()}")
            continue
        country, city = parts
        locations.append((country.strip(), city.strip()))

# Generate redirect pages
with open(SITEMAP_FILE, "a", encoding="utf-8") as sitemap:
    for country, city in locations:
        filename = f"{country.lower()}_{city.lower().replace(' ', '_')}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="refresh" content="0; url=https://www.respirework.com">
  <meta name="robots" content="noindex, follow">
  <title>{city}, {country} | Respirework</title>
</head>
<body>
  <p>Redirecting to <a href="https://www.respirework.com">https://www.respirework.com</a>...</p>
</body>
</html>
"""
        with open(filepath, "w", encoding="utf-8") as out:
            out.write(html)

        sitemap.write(f"https://www.respirework.com/{filename}\n")
        print(f"✅ Created page: https://www.respirework.com/{filename}")

print(f"\n✅ Done. Total redirect pages created: {len(locations)}")
