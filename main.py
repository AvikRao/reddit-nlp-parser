import praw
import json
import re
import yfinance as yf

SUBREDDITS = ("investing", "stocks", "securityanalysis", "finance", "robinhood")
PATTERN = r"\$([a-zA-Z]+)|NYSE:\$?([a-zA-Z]+)|NYSE:\$?([a-zA-Z]+)|(\b[A-Z]{3,4}\b)"

FALSE_MATCHES = {"ETF", "CEO", "IPO", "SEC", "EPS", "NYSE", "USD", "TLDR", "FAQ", "USA", "EDIT", "GDP"}
# TRUE_MATCHES = {"GME", "TSLA", 'AAPL', 'PLTR', 'ARK', "PLUG", "AMZN", "NIO", "SPY", "ARKK", "NVDA", "AMD", "TSM", "MSFT", "ATH", "ITM"}
# TRUE_MATCHES = {"GME", "TSLA", 'AAPL', 'PLTR', 'ARK'}
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
    posts = list(reversed(sorted(list(tickers[ticker]), key=lambda x: x.score)))
    print(posts[0].title, posts[0].score)
    print(posts[1].title, posts[1].score)
    print()

with open("output.json", "w") as f :
    output = {}
    for ticker in max_tickers :
        output[ticker] = {'is_stock': True, 'submissions': []}
        for submission in tickers[ticker] :
            output[ticker]['submissions'].append({"score": submission.score, "title": submission.title, "selftext": submission.selftext, "permalink": submission.permalink, 
            "created_utc": submission.created_utc, "num_comments": submission.num_comments})
    f.write(json.dumps(output, sort_keys=True, indent=4))
    
# max_tickers = ['GME', 'TSLA', 'AAPL']
# ticker_string = " ".join(max_tickers)
# price_data = yf.download(  # or pdr.get_data_yahoo(...
#     # tickers list or string as well
#     tickers = ticker_string,

#     # use "period" instead of start/end
#     # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#     # (optional, default is '1mo')
#     period = "ytd",

#     # fetch data by interval (including intraday if period < 60 days)
#     # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#     # (optional, default is '1d')
#     interval = "1d",

#     # group by ticker (to access via data['SPY'])
#     # (optional, default is 'column')
#     group_by = 'ticker',

#     # adjust all OHLC automatically
#     # (optional, default is False)
#     auto_adjust = True,

#     # use threads for mass downloading? (True/False/Integer)
#     # (optional, default is True)
#     threads = True,
# )

# print(price_data[('GME', 'Open')])

'''
elements in `data`: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
'''