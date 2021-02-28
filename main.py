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
        for submission in list(reversed(sorted(list(tickers[ticker]), key=lambda x: x.score))) :
            output[ticker]['submissions'].append({"score": submission.score, "title": submission.title, "selftext": submission.selftext, "permalink": submission.permalink, 
            "created_utc": submission.created_utc, "num_comments": submission.num_comments})
    f.write(json.dumps(output, sort_keys=True, indent=4))
    
max_tickers = ['GME', 'TSLA', 'AAPL']
ticker_string = " ".join(max_tickers)
price_data = yf.download(    
    tickers = ticker_string,
    period = "ytd",
    interval = "1d",
    group_by = 'ticker',
    auto_adjust = True,
    threads = True,
)

with open("prices.json", "w") as f :

    prices = {}
    for ticker in max_tickers :
        prices[ticker] = {}
        for date in list(price_data[(ticker, 'Close')].keys()) :
            prices[ticker][str(date.date())] = float(price_data[(ticker, 'Close')][date])
    
    f.write(json.dumps(prices, sort_keys=True, indent=4))

# print(list(price_data[('GME', 'Open')].keys())[0].date())

'''
elements in `data`: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
'''