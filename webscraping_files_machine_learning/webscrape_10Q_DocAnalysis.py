import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup as bs
import requests
import time


stock_list = pd.read_csv('Russell3000stocks.csv')
stocks = stock_list['Ticker']


price_list = []
stock_tickers = []
bankrupt_mention = []
decline_mention = []

count = 0
headers = {'User-Agent': 'Mozilla/5.0'}

# BeautifulSoup is sufficient to webscrape the SEC filings 10Q form from MarketWatch.com

for n in range(0,len(stocks)):
    append_next = False
    count += 1

    ticker = str(stocks.values[n])
    all_query_values = []

    # Need to go to the stock ticker 10Q homepage first
    req = requests.get('https://www.marketwatch.com/investing/stock/%s/secfilings?subview=10Q'%ticker, headers=headers)

    soup = bs(req.text, 'html.parser')

    try:
        q10 = soup.find_all('tr')[1]
       # print(len(q10))

    except (IndexError):
        print('INDEX ERROR... retry')
        time.sleep(60)
        req = requests.get('https://www.marketwatch.com/investing/stock/%s/secfilings?subview=10Q' % ticker,
                           headers=headers)

        soup = bs(req.text, 'html.parser')
        print(len(soup.find_all('tr')))
        q10 = soup.find_all('tr')[1]
        print(len(q10))

    if len(q10)<10:
        print('Error, less than 10', np.nan)
        stock_tickers.append(ticker)
        bankrupt_mention.append(np.nan)
        decline_mention.append(np.nan)
        continue

    else:
        q10 = q10.find_all('td')[2]


    str_q10 = str(q10)
    splitted = str_q10.split('guid=')

    # Need to get the SEC filing number, not just the stock ticker name to create the correct doc link
    sec_num = splitted[1][0:8]

    final_url = 'https://www.marketwatch.com/investing/stock/'+ticker+'/SecArticle?countryCode=US&guid='+sec_num+'&type=4'
   # print(final_url)
    req = requests.get(final_url,
                       headers=headers)


    soup = bs(req.text, 'html.parser')

    # Directly scrape all text
    x = str(soup.find_all('div'))
    # all_x = [item.text for item in x]
    # x = ''.join(all_x)

    # Uses regex to get positive or negative sentiment analysis based on n-gram term frequency
    positive = re.findall('(optimis\w*|not affected|excit|excellen|'
                          'well.?position|low\w* risk|grown by|eager|increas\w* demand)', x)
    counted_p = len(positive)
   # print(positive)

    negative = re.findall('(ha\w* advers|revenue declin|profit declin|unsuccessful|growth declin|high\w* risk)', x)
    counted_n = len(negative)
   # print(negative)

    print(count, ticker, counted_p, counted_n)

    stock_tickers.append(ticker)
    bankrupt_mention.append(counted_p)
    decline_mention.append(counted_n)


    if count % 10 == 0:
        df = pd.DataFrame()
        df['Ticker'] = stock_tickers
        df['Bankruptcy Mentioned?'] = bankrupt_mention
        df['Difficulty Mentioned?'] = decline_mention
        df.to_csv('10Q_sentiment_analysis.csv',index = None)


df = pd.DataFrame()
df['Ticker'] = stock_tickers
df['Bankruptcy Mentioned?'] = bankrupt_mention
df['Decline Mentioned?'] = decline_mention
df.to_csv('10Q_sentiment_analysis.csv',index = None)

