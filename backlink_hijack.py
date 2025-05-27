import requests
from bs4 import BeautifulSoup
import pandas as pd

competitor_url = "COMPETITOR_POST_URL"
your_url = "YOUR_BETTER_POST_URL"

# Get backlinks from Ahrefs API
ahrefs_api = f"https://api.ahrefs.com/v2/backlinks?target={competitor_url}"
response = requests.get(ahrefs_api).json()

# Extract contact emails and send pitches
for link in response['backlinks']:
    domain = link['url_from']
    try:
        contact_page = requests.get(f"{domain}/contact").text
        email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', contact_page).group()
        # Send email via SendGrid API
        requests.post("https://api.sendgrid.com/v3/mail/send", 
                     json={"personalizations": [{"to": [{"email": email}]}],
                           "content": [{"type": "text/plain", "value": f"Hi, we improved this resource: {your_url}"}]})
    except:
        continue
