import os
import random
from datetime import datetime

os.makedirs("pages", exist_ok=True)

with open("topics.txt", "r") as f:
    topics = [line.strip() for line in f if line.strip()]

with open("locations.txt", "r") as f:
    locations = [line.strip() for line in f if line.strip()]

def slugify(text):
    return text.lower().replace(",", "").replace(" ", "_")

def generate_content(topic, location):
    country, city = location.split(",")
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{topic} News in {city}, {country}</title>
        <meta name="description" content="Latest updates about {topic} in {city}, {country}. Stay informed with RespireWork.">
        <meta name="keywords" content="{topic}, {city}, {country}, news, trends">
        <meta http-equiv="refresh" content="0; url=https://www.respirework.com">
    </head>
    <body>
        <h1>Redirecting to RespireWork...</h1>
        <p>If not redirected, <a href="https://www.respirework.com">click here</a>.</p>
    </body>
    </html>
    """

# Choose a random topic/location each time to keep unique
topic = random.choice(topics)
location = random.choice(locations)
filename = f"{slugify(topic)}_{slugify(location)}.html"
filepath = os.path.join("pages", filename)

with open(filepath, "w") as f:
    f.write(generate_content(topic, location))

# Generate or update sitemap
with open("sitemap.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for file in os.listdir("pages"):
        if file.endswith(".html"):
            url = f"https://www.respirework.com/pages/{file}"
            f.write(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{datetime.utcnow().date()}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>\n""")
    f.write('</urlset>')
