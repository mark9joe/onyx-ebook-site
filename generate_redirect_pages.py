import os from datetime import datetime, timezone from openai import OpenAI

Step 1: Load your OpenAI API key

api_key = os.getenv("OPENAI_API_KEY") if not api_key: raise Exception("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)

Step 2: Define paths and data

LOCATIONS_FILE = "locations.txt" OUTPUT_DIR = "docs"  # GitHub Pages uses 'docs' directory os.makedirs(OUTPUT_DIR, exist_ok=True)

Step 3: Load locations

def load_locations(file): locations = [] with open(file, "r", encoding="utf-8") as f: for line in f: parts = line.strip().split(",") if len(parts) != 2: continue locations.append((parts[0].strip(), parts[1].strip())) return locations

locations = load_locations(LOCATIONS_FILE)

Step 4: Generate pages

for country, city in locations: slug = f"{country.lower().replace(' ', '')}{city.lower().replace(' ', '_')}" filename = f"{slug}.html" filepath = os.path.join(OUTPUT_DIR, filename)

try:
    # Step 5: Generate content using GPT-3.5
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an SEO expert writing content for a local landing page."},
            {"role": "user", "content": f"Write SEO content for {city}, {country}. Mention Respirework.com and add some trending topics."}
        ]
    )
    content = response.choices[0].message.content.strip()

    # Step 6: Build the HTML
    html = f"""<!DOCTYPE html>

<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{city}, {country} | Respirework</title>
    <meta name=\"description\" content=\"Explore content from {city}, {country} with Respirework.com\">
</head>
<body>
    <h1>{city}, {country} - Local Insights</h1>
    <div>{content}</div>
    <p>Visit our homepage: <a href=\"https://www.respirework.com\">Respirework</a></p>
    <script>setTimeout(() => window.location.href = 'https://www.respirework.com', 10000);</script>
</body>
</html>"""with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Created: https://www.respirework.com/{filename}")

except Exception as e:
    print(f"❌ Error generating content for {city}, {country}: {e}")

