from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import numpy as np

#Importing a list of stock tickers
stock_list = pd.read_csv('Russell3000stocks.csv')
stocks = stock_list['ticker_3000']

# Need to activate Chrome Driver for Selenium to load webpages
driver = webdriver.Chrome('chromedriver.exe')

stock_ticker = []
stock_name = []
curr_price = []
pred_low = []
pred_avg = []
pred_high = []
num_analyst = []
count = 0

# Loop to iterate through every stock and grab the analyst price target values
# TipRanks uses dynamic javascript website, so Selenium is used to load the webpages first.
for i in range(0,int(len(stocks)/2)):
    ticker = str(stocks.values[i])
    url = 'https://www.tipranks.com/stocks/'+ticker+'/forecast/'
    driver.get(url)
    driver.implicitly_wait(11)

    count += 1
    time.sleep(3)

    try:
        title = driver.find_element_by_class_name('client-components-StockPageTabHeader-StockPageTabHeader__StockPageTabHeader')
    except:
        continue


    try:
        analysts = driver.find_element_by_class_name("client-components-stock-research-analysts-analyst-consensus-style__underHeadline")
        number = int(analysts.text[9:-16])
        #Skip the stock if less than 7 analysts, because not credible
        if number <7:
            continue
    except:
        continue

    try:
        actual_price = driver.find_element_by_class_name('client-components-stock-bar-stock-bar__priceValue')
        found_text =str(actual_price.text[1:6])

        if ',' in found_text:
            found_text = found_text.replace(',',"")

        if found_text[0:2] == '0.':
            continue
    except:
        continue



    try:
        pred_price = driver.find_element_by_class_name('client-components-tipranks-charts-price-target-styles-chart-widget__PriceTargetChartHolder')
        scrap_text = pred_price.text

    except:
        continue

    print(count, ticker, number)
    stock_ticker.append(ticker)
    num_analyst.append(number)
    stock_name.append(title.text[:-31])
    curr_price.append(float(found_text))

    for i,s in enumerate(scrap_text):

        if scrap_text[i] == 'A' and scrap_text[i+1] == 'v':
            found_text = scrap_text[i+9:i+15]
            if ',' in found_text:
                found_text = found_text.replace(',',"")
            if '\n' in found_text:
                found_text = found_text.replace('\nL',"   ")
    pred_avg.append(float(found_text))

    for i, s in enumerate(scrap_text):
        if scrap_text[i] == 'L' and scrap_text[i+1] == 'o':
            found_text = scrap_text[i + 5:i + 11]
            if ',' in found_text:
                found_text = found_text.replace(',', "")
            if '\n' in found_text:
                found_text = found_text.replace('\nH',"   ")
    pred_low.append(float(found_text))


    for i, s in enumerate(scrap_text):
        if scrap_text[i] == 'H' and scrap_text[i+1] == 'i':
            found_text = scrap_text[i+6:i+12]
            if ',' in found_text:
                found_text = found_text.replace(',', "")
            if '\n' in found_text:
                found_text = found_text.replace('\n',"   ")
    pred_high.append(float(found_text))




    #Temporarily save after every 20 stocks
    if count%20 == 0:
        df = pd.DataFrame()
        df['stock_ticker'] = stock_ticker
        df['stock_name'] = stock_name
        df['curr_price'] = curr_price
        df['pred_low'] = pred_low
        df['pred_avg'] = pred_avg
        df['pred_high'] = pred_high
        df['# of Analyst'] = num_analyst
        df['% low/curr'] = [100*(x/y-1) for x,y in zip(pred_low,curr_price)]
        df['% avg/curr'] = [100*(x/y-1) for x,y in zip(pred_avg,curr_price)]
        df['% high/curr'] = [100*(x/y-1) for x,y in zip(pred_high,curr_price)]
        df.to_csv('Stocks_TipRank_partA_800.csv', index=None)



driver.quit()


#Last save
df = pd.DataFrame()
df['stock_ticker'] = stock_ticker
df['stock_name'] = stock_name
df['curr_price'] = curr_price
df['pred_low'] = pred_low
df['pred_avg'] = pred_avg
df['pred_high'] = pred_high
df['# of Analyst'] = num_analyst
df['% low/curr'] = [100*(x/y-1) for x,y in zip(pred_low,curr_price)]
df['% avg/curr'] = [100*(x/y-1) for x,y in zip(pred_avg,curr_price)]
df['% high/curr'] = [100*(x/y-1) for x,y in zip(pred_high,curr_price)]
df.to_csv('Stocks_TipRank_partA_800.csv', index=None)
