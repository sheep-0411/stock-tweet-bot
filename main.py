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

# 環境変数の読み込み
load_dotenv(find_dotenv())

# 辞書オブジェクト。認証に必要な情報をHerokuの環境変数から呼び出している
credential = {
"type": "service_account",
"project_id": os.environ['SHEET_PROJECT_ID'],
"private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
"private_key": os.environ['SHEET_PRIVATE_KEY'],
"client_email": os.environ['SHEET_CLIENT_EMAIL'],
"client_id": os.environ['SHEET_CLIENT_ID'],
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://oauth2.googleapis.com/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
}
print(credential)
# スプレッドシートにアクセス
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential, scope)
gc = gspread.authorize(credentials)
sh = gc.open(file_name)

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

# tickertweet(tickers,start_date,end_date,api,onoff)

# for i in keywords:
#     fav(i,api)

# followdestroy(api)

# for i in follow_list:
#     follow(i,api)

Tickers = df1[df1['bot_name'] == 'sector']
print(Tickers)
# performance(Tickers,api,'セクター別パフォーマンス')
