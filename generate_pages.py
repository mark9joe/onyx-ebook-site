import os
from datetime import datetime, timezone

LOCATIONS_FILE = "locations.txt"
OUTPUT_DIR = "."  # Save in repo root

# Get today’s UTC date
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Load locations
locations = []
with open(LOCATIONS_FILE, "r") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) != 2:
            print(f"⚠️ Skipping invalid line: {line.strip()}")
            continue
        country, city = parts
        locations.append((country.strip(), city.strip()))

# Generate redirect HTML pages in root
for country, city in locations:
    filename = f"{country.lower()}_{city.lower().replace(' ', '_')}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)

    redirect_url = "https://www.respirework.com"
    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="refresh" content="0; url={redirect_url}" />
    <meta name="robots" content="noindex, nofollow" />
    <title>Redirecting...</title>
  </head>
  <body>
    <p>If you are not redirected, <a href="{redirect_url}">click here</a>.</p>
  </body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as out:
        out.write(html)

    print(f"✅ Created page: https://www.respirework.com/{filename}")

print(f"\n✅ Done. Total pages created: {len(locations)}")
