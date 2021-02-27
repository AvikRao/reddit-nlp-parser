import praw
import json

with open("auth.json", "r") as f :
    auth = json.loads(f.read())

reddit = praw.Reddit(client_id=auth["client_id"], client_secret=auth["client_secret"], user_agent=auth["user_agent"])

posts = reddit.subreddit('investing').top(limit=1)
for post in posts :
    print(post.title)