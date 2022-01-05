from tickertweet import tickertweet
from follow_fav import fav, followdestroy, follow
from performance import performance

# Googleスプレッドシートとの連携に必要なライブラリ
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

import yfinance as yf
import pandas as pd
import time
import datetime
import os
import tweepy
from dotenv import find_dotenv, load_dotenv
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
import numpy as np

# 設定
json_file = 'investment-bot-337301-f2a71983033e.json'
file_name = 'python-investment'

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
 
# スプレッドシートにアクセス
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
gc = gspread.authorize(credentials)
sh = gc.open(file_name)

# TwitterAPIの初期設定
load_dotenv(find_dotenv())

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# シートの選択　シートの番号でも名前でもよい
wks1 = sh.worksheet('Ticker_list')
wks2 = sh.worksheet('on_off')
wks3 = sh.worksheet('date')
wks4 = sh.worksheet('keyword')

# シートから全部から読み込み
def get_records(wks):
    record = pd.DataFrame(wks.get_all_records())
    return record

df1 = get_records(wks1)
df2 = get_records(wks2)
df3 = get_records(wks3)
df4 = get_records(wks4)

# リストに変換
tickers = df1['Ticker'].tolist()
start_date = df3[df3['bot_name'] =='ticker-tweet']['start'].tolist()[0].replace('/','-')
end_date = df3[df3['bot_name'] =='ticker-tweet']['end'].tolist()[0].replace('/','-')
onoff = df2[df2['bot_name'] =='ticker-tweet']['select'].tolist()[0]
keywords = df4[df4['bot_name'] == 'fav']['keyword'].tolist()
follow_list = df4[df4['bot_name'] == 'follow']['keyword'].tolist()

tickertweet(tickers,start_date,end_date,api,onoff)

for i in keywords:
    fav(i,api)

followdestroy(api)

for i in follow_list:
    follow(i,api)

Tickers = df1[df1['bot_name'] == 'sector']
print(Tickers)
performance(Tickers,api,'セクター別パフォーマンス')
