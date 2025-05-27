import os
from datetime import datetime, timezone
import openai

# Config
LOCATIONS_FILE = "locations.txt"
TOPICS_FILE = "topics.txt"
OUTPUT_DIR = ""  # root folder for your website files
HOMEPAGE_URL = "https://www.respirework.com"

# Setup OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise Exception("OpenAI API key not found in OPENAI_API_KEY env variable")

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

def generate_ai_content(topic, city, country):
    prompt = (f"Write a brief, engaging and informative summary about {topic} news "
              f"in {city}, {country}. Include interesting facts or latest trends. "
              "Keep it short, around 100 words.")
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        text = response.choices[0].text.strip()
        return text
    except Exception as e:
        print(f"Error generating AI content: {e}")
        return f"No content available for {topic} in {city}, {country}."

count = 0
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

for country, city in locations:
    safe_country = country.lower().replace(" ", "_")
    safe_city = city.lower().replace(" ", "_")
    
    for topic in topics:
        filename = f"{topic}_{safe_city}_{safe_country}.html"
        filepath = os.path.join(OUTPUT_DIR, filename) if OUTPUT_DIR else filename

        ai_content = generate_ai_content(topic, city, country)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{topic.capitalize()} news in {city}, {country} | Respirework</title>
  <meta name="description" content="Latest {topic} news and trends in {city}, {country}." />
</head>
<body>
  <header>
    <h1>{topic.capitalize()} News in {city}, {country}</h1>
  </header>
  <main>
    <article>
      <p>{ai_content}</p>
    </article>
    <section>
      <h2>Visit Our Homepage</h2>
      <p>For more insights, tools, and updates, visit <a href="{HOMEPAGE_URL}">{HOMEPAGE_URL}</a></p>
      <a href="{HOMEPAGE_URL}" style="display:inline-block; padding:10px 20px; background:#007BFF; color:white; text-decoration:none; border-radius:5px;">Go to Respirework</a>
    </section>
  </main>
  <footer>
    <p>Page generated on {today} UTC</p>
  </footer>
</body>
</html>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ Created page: https://www.respirework.com/{filename}")
        count += 1

print(f"\n✅ Done. Total pages created: {count}")
