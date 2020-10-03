from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import numpy as np

stock_list = pd.read_csv('Russell3000stocks.csv')
stocks = stock_list['Ticker']

#stock_list = ['play', 'tsla', 'aapl', 'cnk','nvda']
driver = webdriver.Chrome('chromedriver.exe')

stock_ticker = []
rating = []
news_sentiment = []
count = 0



for i in range(0,int(len(stocks)/2)):
    ticker = str(stocks.values[i])
    url = 'https://www.tipranks.com/stocks/'+ticker+'/stock-analysis/'
    driver.get(url)
    driver.implicitly_wait(12)

    count += 1
    time.sleep(3)

    try:
        find_rating = driver.find_element_by_class_name('client-components-ValueChange-shape__Octagon')
        rating_value = find_rating.text
    except:
        continue



    print(count, ticker, rating_value)
    stock_ticker.append(ticker)
    rating.append(rating_value)


    #Temporarily save after every 20 stocks
    if count%20 == 0:
        df = pd.DataFrame()
        df['stock_ticker'] = stock_ticker
        df['rating'] = rating
        df.to_csv('Stocks_TipRank_partA_Ratings800.csv', index=None)



driver.quit()



df = pd.DataFrame()
df['stock_ticker'] = stock_ticker
df['rating'] = rating
df.to_csv('Stocks_TipRank_partA_Ratings800.csv', index=None)
