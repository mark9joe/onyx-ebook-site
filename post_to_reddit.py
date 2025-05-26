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

# ✅ Safe subreddits
link_subreddits = [
    "FreeEBOOKS",
    "FreeBooksOnline"
]

text_subreddits = [
    "selfpromotion",
    "indieauthors"
]

# Rotating post titles
titles = [
    "🔥 Onyx Storm: A Fantasy Book Lovers’ Must-Read!",
    "New eBook Just Dropped — Dragons, Magic & Rebellion Await!",
    "Get Your Digital Copy of Onyx Storm — Now Live!",
    "Epic Fantasy Adventure with Dragons — Read Onyx Storm Today!",
    "Don’t Miss This Book: The Empyrean Series Continues!"
]

# Link and description
url = "https://www.respirework.com"
description = (
    "Check out this epic fantasy book — **Onyx Storm (The Empyrean #3)**!\n\n"
    "Dragons, rebellion, magic — and a world waiting to be saved.\n\n"
    f"Read now: {url}"
)

# Randomly decide post type
post_type = random.choice(["link", "text"])

# Post as link
if post_type == "link":
    subreddit_name = random.choice(link_subreddits)
    title = random.choice(titles)
    try:
        subreddit = reddit.subreddit(subreddit_name)
        submission = subreddit.submit(title=title, url=url)
        print(f"✅ Link posted to r/{subreddit_name}: {submission.permalink}")
    except Exception as e:
        print(f"❌ Failed to post link: {e}")

# Post as text
else:
    subreddit_name = random.choice(text_subreddits)
    title = random.choice(titles)
    try:
        subreddit = reddit.subreddit(subreddit_name)
        submission = subreddit.submit(title=title, selftext=description)
        print(f"✅ Text posted to r/{subreddit_name}: {submission.permalink}")
    except Exception as e:
        print(f"❌ Failed to post text: {e}")
