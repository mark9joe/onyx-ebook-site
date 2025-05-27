import os
import openai

# Get your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise Exception("OpenAI API key not found in OPENAI_API_KEY environment variable")

# List of locations you want pages for (change or load from your file)
locations = [
    ("Ireland", "Dublin"),
    ("USA", "New York"),
    ("UK", "London"),
]

OUTPUT_DIR = "redirect_pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)

homepage_url = "https://www.respirework.com"

for country, city in locations:
    filename = f"{country.lower()}_{city.lower().replace(' ', '_')}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)

    prompt = f"Write a short SEO-friendly introduction about news and events in {city}, {country}. Also promote the website {homepage_url}."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        content = response.choices[0].text.strip()
    except Exception as e:
        content = f"Sorry, content could not be generated. Error: {e}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{city}, {country} | Respirework</title>
  <meta http-equiv="refresh" content="10; url={homepage_url}" />
</head>
<body>
  <h1>News and updates from {city}, {country}</h1>
  <p>{content}</p>
  <p>If you are not redirected automatically, <a href="{homepage_url}">click here to visit Respirework</a>.</p>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Created redirect page: {filepath}")

print("\n✅ All pages generated successfully.")
