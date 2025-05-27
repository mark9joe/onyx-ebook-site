import os
from datetime import datetime, timezone

# Paths
LOCATIONS_FILE = "onyx-ebook-site/locations.txt"
OUTPUT_DIR = "generated_pages"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get today's date in UTC
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

# Generate HTML pages
for country, city in locations:
    filename = f"{country.lower()}_{city.lower().replace(' ', '_')}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{city}, {country} | Respirework</title>
</head>
<body>
  <h1>Welcome from {city}, {country}!</h1>
  <p>This local landing page was generated on {today}.</p>
</body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as out:
        out.write(html)

    print(f"✅ Created page: {filepath}")

print(f"\n✅ Done. Total pages created: {len(locations)}")
