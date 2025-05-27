import praw
reddit = praw.Reddit(client_id='YOUR_ID', client_secret='YOUR_SECRET')

for submission in reddit.subreddit("YOUR_NICHE").hot(limit=10):
    if submission.created_utc > (time.time() - 10800):  # 3 hours old
        submission.reply(f"Great question! We covered this here: {your_url}")
