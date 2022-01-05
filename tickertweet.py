import yfinance as yf
import time
import tweepy
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw

# Tcikerの情報をツイートする。
# Googleスプレッドシート上でbotの起動をコントロールする
def tickertweet(tickers,start_date,end_date,api,onoff):
    if onoff == 'on':

        for i in tickers:
            data = yf.download(i, start=start_date, end=end_date)
            df = data.loc[:,['Close','Volume']]
            df['Volume'] = round(df['Volume']/1000000,2)
            fig, ax1 = plt.subplots(1,1,figsize=(10,8))
            ax2 = ax1.twinx()
            ax1.bar(df.index,df['Volume'],color='lightblue',label='Volume')
            ax2.plot(df['Close'],color='k',label='Price')
            handler1, label1 = ax1.get_legend_handles_labels()
            handler2, label2 = ax2.get_legend_handles_labels()
            ax1.legend(handler1+handler2,label1+label2,borderaxespad=0)
            ax1.set_ylabel('M') 
            ax2.set_ylabel('$') 
            ax1.grid(True)
            img_name = 'img.png'
            fig.savefig(img_name,dpi=250)

            data = yf.Ticker(i)
            
            marketCap = '時価総額 ' + '{:,}'.format(round((data.info['marketCap'] / 1000000000),2)) + ' B'
            volume = '出来高 ' + '{:,}'.format(data.info['volume'])
            averageVolume = '平均出来高 ' + '{:,}'.format(data.info['averageVolume'])
            averageVolume10days = '直近10日平均出来高 ' + '{:,}'.format(data.info['averageVolume10days'])
            revenueGrowth = '売上高成長率 ' + '{:.2%}'.format(data.info['revenueGrowth'])
            fiftyDayAverage = '52日平均 ' + '{:,}'.format(round(data.info['fiftyDayAverage'],2))
            numberOfAnalystOpinions = 'アナリスト ' + str(data.info['numberOfAnalystOpinions']) + '人'
            currentPrice = '現在の株価 ' + '{:,}'.format(data.info['currentPrice'])
            targetLowPrice = '目標株価(最低) ' + '{:,}'.format(data.info['targetLowPrice'])
            targetMedianPrice = '目標株価(中央値) ' + '{:,}'.format(data.info['targetMedianPrice'])
            targetHighPrice = '目標株価(最高) ' + '{:,}'.format(data.info['targetHighPrice'])
            PSR = 'PSR ' + str(round((data.info['marketCap']) / (data.quarterly_earnings.tail(1)['Revenue'].iloc[-1]*4),2))
            ticker = i
            
            api.update_status_with_media(
            filename = img_name,
            status = '$' +  ticker + '\n'
            + marketCap + '\n'
            + volume + '\n'
            + averageVolume + '\n'
            + averageVolume10days + '\n'
            + revenueGrowth + '\n'
            + fiftyDayAverage + '\n'
            + numberOfAnalystOpinions + '\n'
            + currentPrice + '\n'
            + targetLowPrice + '\n'
            + targetMedianPrice + '\n'
            + targetHighPrice + '\n'
            + PSR       
            )
            time.sleep(5)




