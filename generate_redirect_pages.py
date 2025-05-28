import os
import requests
from datetime import datetime

# CONFIGURATION
TOGETHER_API_KEY = "your_together_ai_api_key"
BASE_URL = "https://www.respirework.com"
HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}
MODEL = "togethercomputer/llama-2-70b-chat"

# Ensure output directories
os.makedirs("generated_pages", exist_ok=True)

# Load locations and topics
with open("locations.txt", "r") as f:
    locations = [line.strip() for line in f if line.strip()]

with open("topics.txt", "r") as f:
    topics = [line.strip() for line in f if line.strip()]

def get_ai_content(location, topic):
    prompt = f"""
    Generate an HTML article (SEO optimized) with a trending title, meta description, and paragraph content.
    Location: {location}
    Topic: {topic}
    Also include a link to {BASE_URL} in the content.
    Format: Include <title>, <meta name='description'>, <h1>, <p>, and a backlink to {BASE_URL}
    """

    response = requests.post("https://api.together.xyz/v1/chat/completions", headers=HEADERS, json={
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 700
    })

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Failed to fetch content: {response.status_code} - {response.text}")
        return "<html><body>Error generating content.</body></html>"

def create_html_file(filename, content):
    filepath = os.path.join("generated_pages", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created page: {BASE_URL}/{filename}")
    return filepath

sitemap_entries = []

for location in locations:
    for topic in topics:
        slug = f"{topic.lower().replace(' ', '_')}_{location.lower().replace(' ', '_').replace(',', '_')}"
        filename = f"{slug}.html"
        html_content = get_ai_content(location, topic)
        filepath = create_html_file(filename, html_content)

        full_url = f"{BASE_URL}/{filename}"
        sitemap_entries.append(f"  <url><loc>{full_url}</loc><lastmod>{datetime.utcnow().isoformat()}Z</lastmod></url>")

# Write sitemap
sitemap_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{os.linesep.join(sitemap_entries)}
</urlset>
"""
with open("generated_pages/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)
print("Generated sitemap.xml")

# Optionally ping search engines
ping_url = f"https://www.google.com/ping?sitemap={BASE_URL}/sitemap.xml"
try:
    ping_response = requests.get(ping_url)
    print("Pinged Google: ", ping_response.status_code)
except Exception as e:
    print("Failed to ping Google", e)

# RSS Feed Generation (Optional)
rss_items = []
for entry in sitemap_entries:
    rss_items.append(f"""
    <item>
        <title>{entry}</title>
        <link>{entry}</link>
        <description>AI generated content about trends</description>
        <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
    </item>
    """)

rss_feed = f"""
<rss version="2.0">
<channel>
<title>RespireWork AI Pages</title>
<link>{BASE_URL}</link>
<description>Latest trending AI-generated country-based content</description>
{''.join(rss_items)}
</channel>
</rss>
"""

with open("generated_pages/rss.xml", "w", encoding="utf-8") as f:
    f.write(rss_feed)
print("Generated rss.xml")
