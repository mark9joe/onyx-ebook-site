import os import openai from datetime import datetime

Set your homepage URL

homepage_url = "https://www.respirework.com"

Set OpenAI API key from environment variable

openai.api_key = os.getenv("OPENAI_API_KEY") if not openai.api_key: raise Exception("OpenAI API key not found in OPENAI_API_KEY environment variable")

Define the list of (country, city)

locations = [ ("Ireland", "Dublin"), ("USA", "New York"), ("UK", "London"), ("Germany", "Berlin") ]

Output directory is the root of the repo

OUTPUT_DIR = "."

def generate_html(city, country, content): return f"""<!DOCTYPE html>

<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{city}, {country} | Respirework</title>
  <meta http-equiv=\"refresh\" content=\"10; url={homepage_url}\">
</head>
<body>
  <h1>Welcome from {city}, {country}!</h1>
  <p>{content}</p>
  <p>If you're not redirected automatically, <a href=\"{homepage_url}\">click here</a>.</p>
</body>
</html>"""Loop through each location and create a page

for country, city in locations: prompt = f"Write a short paragraph promoting the website {homepage_url} for visitors from {city}, {country}." try: response = openai.Completion.create( engine="text-davinci-003", prompt=prompt, max_tokens=150, temperature=0.7 ) content = response.choices[0].text.strip() except Exception as e: content = f"Content could not be loaded due to an error: {e}"

filename = f"{country.lower()}_{city.lower().replace(' ', '_')}.html"
filepath = os.path.join(OUTPUT_DIR, filename)
with open(filepath, "w", encoding="utf-8") as f:
    f.write(generate_html(city, country, content))

print(f"✅ Created page: {homepage_url}/{filename}")

print("\nAll pages generated successfully.")

