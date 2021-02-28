from django.shortcuts import render
from django.http import HttpResponse, Http404
import praw
import json
import urllib

# Create your views here.
def index(request): 

    with open("stocks.json", "r") as f :
        stocks = json.loads(f.read())

    with open("infos.json", "r") as f :
        infos = json.loads(f.read())

    with open("prices.json", "r") as f :
        prices = json.loads(f.read())

    print(prices)
    stock_keys = list(stocks.keys())
    info_keys = list(infos.keys())

    context = {"stock1_name": stock_keys[0], "stock2_name": stock_keys[1], "stock3_name": stock_keys[2], "stock1_data": stocks[stock_keys[0]], "stock2_data": stocks[stock_keys[1]], "stock3_data": stocks[stock_keys[2]],
    "info1_name": info_keys[0], "info2_name": info_keys[1], "info3_name": info_keys[2], "info1_data": infos[info_keys[0]], "info2_data": infos[info_keys[1]], "info3_data": infos[info_keys[2]], "prices": prices}
    
    return render(request, 'main/index.html', context)

def details(request, path):

    # path = urllib.parse.unquote(path)
    # print(path)

    with open("stocks.json", "r") as f :
        stocks = json.loads(f.read())

    with open("infos.json", "r") as f :
        infos = json.loads(f.read())

    with open("prices.json", "r") as f :
        prices = json.loads(f.read())

    if path.upper() in stocks :
        stock = stocks[path]
        stock['submissions'] = stock['submissions'][:5]
        info = False
    elif path in infos :
        info = infos[path]
        info['submissions'] = info['submissions'][:5]
        stock = False
    else  :
        raise Http404("This page doesn't exist.")
    context = {"topic": path, "stock": stock, "info": info, "prices": prices}
    return render(request, 'main/details.html', context)