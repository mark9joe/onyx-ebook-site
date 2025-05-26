import os
import praw

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    username=os.getenv("REDDIT_USER"),
    password=os.getenv("REDDIT_PASS"),
    user_agent=os.getenv("REDDIT_AGENT")
)

subreddit = reddit.subreddit("selfpromotion")
title = "🔥 Just Released: Onyx Storm - Epic Fantasy eBook!"
url = "https://www.respirework.com"

submission = subreddit.submit(title=title, url=url)
print("✅ Posted to:", submission.permalink)
