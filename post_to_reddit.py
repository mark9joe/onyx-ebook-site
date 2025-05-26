import os
import random
import praw

# Reddit authentication
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    username=os.getenv("REDDIT_USER"),
    password=os.getenv("REDDIT_PASS"),
    user_agent=os.getenv("REDDIT_AGENT")
)

# Safe text-post subreddits (no flair required)
text_subreddits = [
    "selfpromotion",
    "indieauthors"
]

titles = [
    "🔥 Onyx Storm: A Fantasy Book Lovers’ Must-Read!",
    "New eBook Just Dropped — Dragons, Magic & Rebellion Await!",
    "Epic Fantasy Adventure with Dragons — Read Onyx Storm Today!"
]

description = (
    "Discover an epic fantasy novel: **Onyx Storm (The Empyrean #3)**!\n\n"
    "Featuring dragons, rebellion, and magic — it's the third chapter in a bestselling saga.\n\n"
    "**Read more:** https://www.respirework.com"
)

# Choose subreddit + title
subreddit_name = random.choice(text_subreddits)
title = random.choice(titles)

try:
    submission = reddit.subreddit(subreddit_name).submit(
        title=title,
        selftext=description
    )
    print(f"✅ Successfully posted to r/{subreddit_name}: {submission.permalink}")
except Exception as e:
    print(f"❌ Failed to post: {e}")
