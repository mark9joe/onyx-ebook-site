import os from datetime import datetime, timezone

Input file with list of locations

LOCATIONS_FILE = "locations.txt"

Where to generate the HTML files (root of repo)

OUTPUT_DIR = "."

Base website URL

BASE_URL = "https://www.respirework.com"

Get current UTC date

today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

Read and parse locations

locations = [] with open(LOCATIONS_FILE, "r") as f: for line in f: parts = line.strip().split(",") if len(parts) != 2: print(f"⚠️ Skipping invalid line: {line.strip()}") continue country, city = parts locations.append((country.strip(), city.strip()))

Generate redirect pages

sitemap_entries = [] for country, city in locations: filename = f"{country.lower()}{city.lower().replace(' ', '')}.html" filepath = os.path.join(OUTPUT_DIR, filename)

redirect_html = f"""<!DOCTYPE html>

<html lang=\"en\">
  <head>
    <meta http-equiv=\"refresh\" content=\"0; url={BASE_URL}\" />
    <meta name=\"robots\" content=\"noindex, nofollow\" />
    <title>Redirecting...</title>
  </head>
  <body>
    <p>Redirecting to <a href=\"{BASE_URL}\">{BASE_URL}</a>...</p>
  </body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(redirect_html)print(f"✅ Created page: {BASE_URL}/{filename}")
sitemap_entries.append(f"{BASE_URL}/{filename}")

Optional: Save to sitemap file

sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.txt") with open(sitemap_path, "w", encoding="utf-8") as f: f.write("\n".join(sitemap_entries))

print(f"\n✅ All {len(locations)} pages redirect to {BASE_URL}") print(f"Sitemap saved to: {sitemap_path}")

                                                                 
