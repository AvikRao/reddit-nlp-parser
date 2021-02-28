from django.shortcuts import render
from django.http import HttpResponse
import praw
import json

SUBREDDITS = ("investing", "stocks")

with open("auth.json", "r") as f :
    auth = json.loads(f.read())

reddit = praw.Reddit(client_id=auth["client_id"], client_secret=auth["client_secret"], user_agent=auth["user_agent"])

data = []

for subreddit in SUBREDDITS :

    praw_subreddit = reddit.subreddit(subreddit)

    top_posts_week = praw_subreddit.top("week")
    for post in top_posts_week :
        data.append(post)

print(len(data))

# Create your views here.
def index(request): 
    context = {"main": "Hello world!", "test": 5}
    return render(request, 'main/index.html', context)

def details(request, path):
    context = {"topic": path, "data": data[:4]}
    return render(request, 'main/details.html', context)