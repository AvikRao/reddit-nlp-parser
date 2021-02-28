import praw
import json
import re

SUBREDDITS = ("investing", "stocks", "securityanalysis", "finance", "robinhood")
PATTERN = r"\$([a-zA-Z]+)|NYSE:\$?([a-zA-Z]+)|NYSE:\$?([a-zA-Z]+)|(\b[A-Z]{3,4}\b)"

FALSE_MATCHES = {"ETF", "CEO", "IPO", "SEC", "EPS", "NYSE", "USD", "TLDR", "FAQ", "USA", "EDIT", "GDP"}
# TRUE_MATCHES = {"GME", "TSLA", 'AAPL', 'PLTR', 'ARK', "PLUG", "AMZN", "NIO", "SPY", "ARKK"}
TRUE_MATCHES = set()

with open("auth.json", "r") as f :
    auth = json.loads(f.read())

with open("tickers.json", "r") as f :
    tickers_list = json.loads(f.read())

reddit = praw.Reddit(client_id=auth["client_id"], client_secret=auth["client_secret"], user_agent=auth["user_agent"])

data = set()
tickers = {}

for subreddit in SUBREDDITS :

    praw_subreddit = reddit.subreddit(subreddit)

    top_posts_week = praw_subreddit.top("week", limit=100)
    for post in top_posts_week :
        data.add(post)
    
    hot_posts = praw_subreddit.hot(limit=100)
    for post in hot_posts :
        data.add(post)

for post in data :
    string = post.title + " \n " + post.selftext
    matches = re.findall(PATTERN, string)
    for ticker in matches :
        ticker_parsed = [x for x in ticker if x][0].upper()
        if ticker_parsed not in tickers :
            tickers[ticker_parsed] = set()
        tickers[ticker_parsed].add(post)

max_tickers = ["", "", ""]
max_counts = [0, 0, 0]

for ticker in tickers :
    if ticker not in FALSE_MATCHES and ticker not in TRUE_MATCHES and ticker in tickers_list:
        if len(tickers[ticker]) > max_counts[0] :
            max_counts[2] = max_counts[1]
            max_counts[1] = max_counts[0]
            max_tickers[2] = max_tickers[1]
            max_tickers[1] = max_tickers[0]
            max_counts[0] = len(tickers[ticker])
            max_tickers[0] = ticker
        elif len(tickers[ticker]) > max_counts[1] :
            max_counts[2] = max_counts[1]
            max_tickers[2] = max_tickers[1]
            max_counts[1] = len(tickers[ticker])
            max_tickers[1] = ticker
        elif len(tickers[ticker]) > max_counts[2] :
            max_counts[2] = len(tickers[ticker])
            max_tickers[2] = ticker

print(max_tickers)
print(max_counts)

print()
for ticker in max_tickers :
    print(tickers[ticker].pop().title)
    print(tickers[ticker].pop().title)


'''
elements in `data`: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
'''