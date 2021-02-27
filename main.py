import praw
import json
import pandas as pd

SUBREDDITS = ("investing", "stocks")

with open("auth.json", "r") as f :
    auth = json.loads(f.read())

reddit = praw.Reddit(client_id=auth["client_id"], client_secret=auth["client_secret"], user_agent=auth["user_agent"])

data = set()

for subreddit in SUBREDDITS :

    praw_subreddit = reddit.subreddit(subreddit)

    top_posts_week = praw_subreddit.top("week")
    for post in top_posts_week :
        data.add(post)
    
    hot_posts = praw_subreddit.hot()
    for post in hot_posts :
        data.add(post)

print(len(data))

'''
elements in `data`: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
'''