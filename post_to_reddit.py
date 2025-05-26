import os
import random
import praw

# Authenticate Reddit client using environment variables
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    username=os.getenv("REDDIT_USER"),
    password=os.getenv("REDDIT_PASS"),
    user_agent=os.getenv("REDDIT_AGENT")
)

# Subreddits grouped by post type
link_subreddits = [
    "FreeEBOOKS",
    "BookPromo",
    "FreeBooksOnline",
    "PromoteYourBusiness"
]

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

# Website to link to
url = "https://www.respirework.com"
description = (
    "Check out this epic fantasy book — **Onyx Storm (The Empyrean #3)**!\n\n"
    "Dragons, rebellion, magic — and a world waiting to be saved.\n\n"
    f"Read now: {url}"
)

# Randomly choose type
post_type = random.choice(["link", "text"])

if post_type == "link":
    subreddit_name = random.choice(link_subreddits)
    title = random.choice(titles)
    try:
        subreddit = reddit.subreddit(subreddit_name)
        submission = subreddit.submit(title=title, url=url)
        print(f"✅ Link post to r/{subreddit_name} succeeded: {submission.permalink}")
    except Exception as e:
        print(f"❌ Failed to post link: {e}")

else:
    subreddit_name = random.choice(text_subreddits)
    title = random.choice(titles)
    try:
        subreddit = reddit.subreddit(subreddit_name)
        submission = subreddit.submit(title=title, selftext=description)
        print(f"✅ Text post to r/{subreddit_name} succeeded: {submission.permalink}")
    except Exception as e:
        print(f"❌ Failed to post text: {e}")
