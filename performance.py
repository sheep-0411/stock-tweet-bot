import tweepy
import datetime
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import time
import numpy as np

results = []

def performance(Tickers,api,title):
    
    figsize_px = np.array([1200, 675])
    dpi = 100
    figsize_inch = figsize_px / dpi
    fig, ax = plt.subplots(figsize=figsize_inch, dpi=dpi) #ベースを作る
    ax.set_ylabel('%') #y軸のラベルを設定する

    today = datetime.date.today()
    start_date = '2022-' + str(today.month) + '-1'
    end_date = str(today.year) + '-12-31'

    for name,ticker in zip(Tickers['Name'], Tickers['Ticker']):
        data = yf.download(ticker, start = start_date, end = end_date)
        stn = data['Close'][0] #一番古い日の株価を基準にする
        rate = data['Close']*100/stn #基準からの増加率を%で計算
        result = data.tail(1)['Close']*100/stn #基準からの増加率を%で計算
        results.append(round(result[0],2))
        ax.plot(rate,label=name) #グラフを重ねて描写していく
    Tickers['growth'] = results
    df = Tickers.sort_values('growth',ascending=False).reset_index(drop=True)
    print(df)
    ax.set_title(start_date + '~')
    ax.legend()
    ax.grid()
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=10)
    fig.savefig('img1.png', bbox_inches='tight')

    file_names = ['img1.png']
    media_ids = []
    tag = ''
    text = ''

    for filename in file_names:
        res = api.media_upload(filename)
        media_ids.append(res.media_id)

    for name,ticker,growth in zip(df['Name'], df['Ticker'],df['growth']):

        tag = tag + '$' + ticker + ' '

        text = text + name + ' ' + str(growth) + '%' + '\n'
    
    api.update_status(
        status= title + '(' + start_date + '~' + ')' +  '\n' + text + tag,
        media_ids= media_ids,
    )




        
 
