import os
import openai
from datetime import datetime, timezone

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("OpenAI API key not found in OPENAI_API_KEY env variable")

openai.api_key = api_key

# File paths
LOCATIONS_FILE = "locations.txt"
OUTPUT_DIR = "."

# Date for metadata
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Load locations
with open(LOCATIONS_FILE, "r") as f:
    locations = [line.strip() for line in f if line.strip()]

# Generate redirect pages with AI content
for entry in locations:
    parts = entry.split(",")
    if len(parts) != 2:
        print(f"⚠️ Invalid entry in locations.txt: {entry}")
        continue

    country, city = parts[0].strip(), parts[1].strip()
    filename = f"{country.lower()}_{city.lower().replace(' ', '_')}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # AI content
    topic = f"latest trending news, events, and culture from {city}, {country}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful content writer."},
                {"role": "user", "content": f"Write an SEO-optimized 150-word intro about {topic}."}
            ]
        )
        content = response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Error fetching content for {entry}: {e}")
        continue

    # HTML with redirect and promotion
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{city}, {country} | Respirework</title>
  <meta http-equiv="refresh" content="10; url=https://www.respirework.com">
  <meta name="description" content="Trending local content for {city}, {country} from Respirework.">
</head>
<body>
  <h1>Trending in {city}, {country}</h1>
  <p>{content}</p>
  <p>You’ll be redirected to our homepage shortly: <a href="https://www.respirework.com">Respirework</a></p>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Created page: https://www.respirework.com/{filename}")

print(f"\n✅ Done. Total pages created: {len(locations)}")
