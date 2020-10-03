import numpy as np
import re
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd


stock_list = pd.read_csv('Russell3000stocks.csv')
stocks = stock_list['Ticker']
count = 0

zacks_rank = []
value_score = []
growth_score = []
momentum_score = []
overall_score = []
industry_rank = []
ticker_list= []

# Uses Beautiful Soup to webscrape data from Zacks.com

for n in range(830,len(stocks)):  #Zack's Ratings
    features = []
    time.sleep(2)
    count += 1
    ticker = str(stocks.values[n])
    print(count, ticker)

    headers = {'User-Agent': 'Chrome/85.0.4183.102'}
    req = requests.get('https://www.zacks.com/stock/quote/%s'%ticker, headers=headers)
    soup = bs(req.text, 'html.parser')

    td = soup.find_all('p', attrs={'class':'rank_view'})
    alphabet_score = td[1].find_all('span')

    ticker_list.append(ticker)
    try:
        zacks_rank.append(td[0].text.split()[-1])
        value_score.append(alphabet_score[0].text)
        growth_score.append(alphabet_score[2].text)
        momentum_score.append(alphabet_score[4].text)
        overall_score.append(alphabet_score[6].text)

    except(IndexError):
        zacks_rank.append(np.nan)
        value_score.append(np.nan)
        growth_score.append(np.nan)
        momentum_score.append(np.nan)
        overall_score.append(np.nan)
    try:
        industry_rank.append(np.round(int(td[2].text.split()[-1][:-1])/int(td[2].text.split()[2][1:]),1))
    except(ValueError):
        industry_rank.append(np.nan)

    if count%10 == 0:
        df = pd.DataFrame()
        df['ticker'] = ticker_list
        df['zacks rank'] = zacks_rank
        df['value score'] = value_score
        df['growth score'] = growth_score
        df['momentum score'] = momentum_score
        df['overall score'] = overall_score
        df['industry rank'] = industry_rank

        df.to_csv('Stocks_zacks_830rank_Q2.csv', index=None)

df = pd.DataFrame()
df['ticker'] = ticker_list
df['zacks rank'] = zacks_rank
df['value score'] = value_score
df['growth score'] = growth_score
df['momentum score'] = momentum_score
df['overall score'] = overall_score
df['industry rank'] = industry_rank

df.to_csv('Stocks_zacks_830rank_Q2.csv', index=None)