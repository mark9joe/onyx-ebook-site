import os
import feedparser
from urllib.parse import urlparse
from pathlib import Path

RSS_FEED = "https://www.respirework.com/rss/rebecca-yarros.xml"
OUTPUT_DIR = "redirect_pages"

feed = feedparser.parse(RSS_FEED)
os.makedirs(OUTPUT_DIR, exist_ok=True)

redirect_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0;url={target}">
  <script>
    window.location.href = "{target}";
  </script>
  <title>Redirecting...</title>
</head>
<body>
  <p>Redirecting to <a href="{target}">{target}</a></p>
</body>
</html>
"""

for entry in feed.entries:
    slug = urlparse(entry.link).path.strip("/")
    filename = os.path.join(OUTPUT_DIR, slug, "index.html")
    Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(redirect_template.format(target=entry.link))
