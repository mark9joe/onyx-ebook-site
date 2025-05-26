import os
import random
import praw

# Authenticate with Reddit
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    username=os.getenv("REDDIT_USER"),
    password=os.getenv("REDDIT_PASS"),
    user_agent=os.getenv("REDDIT_AGENT")
)

# Subreddits that allow text posts from new users
text_subreddits = [
    "selfpromotion",
    "indieauthors",
    "GetMoreViewsYT",
    "MarketYourBook"
]

# Post titles
titles = [
    "🔥 Onyx Storm: A Fantasy Book Lovers’ Must-Read!",
    "New eBook Just Dropped — Dragons, Magic & Rebellion Await!",
    "Get Your Digital Copy of Onyx Storm — Now Live!",
    "Epic Fantasy Adventure with Dragons — Read Onyx Storm Today!",
    "Don’t Miss This Book: The Empyrean Series Continues!"
]

# Post description with your link embedded
description = (
    "Check out this epic fantasy book — **Onyx Storm (The Empyrean #3)**!\n\n"
    "Dragons, rebellion, magic — and a world waiting to be saved.\n\n"
    "Grab your copy: https://www.respirework.com"
)

# Randomly choose subreddit and title
subreddit_name = random.choice(text_subreddits)
title = random.choice(titles)

# Submit text post
try:
    subreddit = reddit.subreddit(subreddit_name)
    submission = subreddit.submit(title=title, selftext=description)
    print(f"✅ Text post succeeded: r/{subreddit_name} — {submission.permalink}")
except Exception as e:
    print(f"❌ Failed to post text: {e}")
