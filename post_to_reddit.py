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

# List of subreddits that allow promotions
subreddits = [
    "selfpromotion",
    "indieauthors",
    "FreeBooksOnline",
    "GetMoreViewsYT",
    "MarketYourBook"
]

# Titles to rotate
titles = [
    "🔥 Onyx Storm: A Fantasy Book Lovers’ Must-Read!",
    "New eBook Just Dropped — Dragons, Magic & Rebellion Await!",
    "Get Your Digital Copy of Onyx Storm — Now Live!",
    "Epic Fantasy Adventure with Dragons — Read Onyx Storm Today!",
    "Don’t Miss This Book: The Empyrean Series Continues!"
]

# Randomly choose subreddit and title
selected_subreddit = random.choice(subreddits)
selected_title = random.choice(titles)
link_url = "https://www.respirework.com"

# Post to Reddit
try:
    submission = reddit.subreddit(selected_subreddit).submit(
    title=selected_title,
    selftext="Check out this epic fantasy book — Onyx Storm (The Empyrean #3)! Featuring dragons, rebellion, and magic.\n\nRead more: https://www.respirework.com"
)
    print(f"✅ Successfully posted to r/{selected_subreddit}: {submission.permalink}")
except Exception as e:
    print(f"❌ Failed to post: {e}")
