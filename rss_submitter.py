import requests

rss_feeds = [
    "https://www.respirework.com/rss/empyrean-series.xml",
    "https://www.respirework.com/rss/rebecca-yarros.xml"
]

aggregators = [
    "http://rpc.pingomatic.com/",
    "https://www.blogdigger.com/RPC2",
    "https://ping.feedburner.com/",
    "https://rpc.twingly.com/"
]

for feed_url in rss_feeds:
    for ping_url in aggregators:
        try:
            response = requests.post(ping_url, data={"url": feed_url})
            print(f"Pinged {ping_url} for {feed_url}: {response.status_code}")
        except Exception as e:
            print(f"Failed to ping {ping_url}: {e}")
