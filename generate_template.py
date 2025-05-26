import random
from datetime import datetime

titles = [
    "Breaking Update from RespireWork",
    "Fresh News Just In",
    "Important Announcement You Missed",
    "Auto-Recovered Page by System",
    "New Info Available Now",
    "Your Requested Page is Ready",
    "Automatically Restored Article",
    "Exclusive RespireWork Coverage",
    "Archived Info Brought Back",
    "Latest Development Revealed"
]

descriptions = [
    "We've generated this page to make sure you never miss an important update again.",
    "This article was restored automatically by our system to keep you informed.",
    "The original page couldn't be found, but we've recovered this version for you.",
    "Enjoy our freshly generated content tailored for curious readers like you.",
    "RespireWork brings you back to speed with a regenerated article.",
    "Thanks for visiting. This page has been re-created based on user interest.",
    "This auto-generated page serves as a placeholder while we restore the original.",
    "We noticed you were searching for this topic — here’s a refreshed version.",
    "This content is part of our ongoing auto-healing system for broken links.",
    "The information you’re looking for is now restored and available again."
]

images = [
    "https://source.unsplash.com/featured/?technology",
    "https://source.unsplash.com/featured/?news",
    "https://source.unsplash.com/featured/?cyber",
    "https://source.unsplash.com/featured/?innovation",
    "https://source.unsplash.com/featured/?global"
]

def generate_template(slug):
    title = random.choice(titles)
    description = random.choice(descriptions)
    image_url = random.choice(images)
    date = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{image_url}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://www.respirework.com/{slug}">
</head>
<body>
  <div style="max-width: 720px; margin: auto; font-family: Arial, sans-serif;">
    <h1>{title}</h1>
    <p><em>Generated on {date}</em></p>
    <img src="{image_url}" alt="Related image" style="width:100%; border-radius: 6px; margin-bottom: 20px;" />
    <p>{description}</p>
    <p>This page was generated automatically because the original content was missing or removed.</p>
    <hr />
    <p><a href="https://www.respirework.com">← Back to RespireWork Homepage</a></p>
  </div>
</body>
</html>
"""
    return html
