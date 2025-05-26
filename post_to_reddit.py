import os
import random
import praw

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    username=os.getenv("REDDIT_USER"),
    password=os.getenv("REDDIT_PASS"),
    user_agent=os.getenv("REDDIT_AGENT")
)

titles = [
    "🔥 Onyx Storm: A Fantasy Book Lovers’ Must-Read!",
    "New eBook Just Dropped — Dragons, Magic & Rebellion Await!"
]

description = (
    "Discover the fantasy saga **Onyx Storm (The Empyrean #3)**.\n\n"
    "Epic dragons, rebellion, magic — read it now: https://www.respirework.com"
)

# Post to your own profile
title = random.choice(titles)
try:
    submission = reddit.subreddit("u_" + reddit.user.me().name).submit(
        title=title,
        selftext=description
    )
    print(f"✅ Posted to your Reddit profile: {submission.permalink}")
except Exception as e:
    print(f"❌ Failed: {e}")
