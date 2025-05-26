import feedparser
import os

# Define your RSS feed URL (replace with your actual RSS feed link)
rss_url = 'https://www.respirework.com/rss/rebecca-yarros.xml'

# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Generate the redirect HTML for each post
for entry in feed.entries:
    title = entry.title
    link = entry.link  # Link to the original article
    
    # Create a new HTML file for the redirect
    redirect_file = f"redirects/{title.replace(' ', '_')}.html"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="0; url={link}">
        <title>Redirecting...</title>
    </head>
    <body>
        <p>If you are not redirected, click <a href="{link}">here</a>.</p>
    </body>
    </html>
    """
    
    # Make sure the redirects folder exists
    if not os.path.exists('redirects'):
        os.makedirs('redirects')
    
    # Write the redirect HTML to the file
    with open(redirect_file, 'w') as f:
        f.write(html_content)

    print(f"Generated redirect for {title} at {redirect_file}")
