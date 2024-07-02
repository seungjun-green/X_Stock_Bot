import yfinance as yf
from datetime import datetime
from pytz import timezone
from twitter import *
from brain import *
import time
import requests
from datetime import date


def is_market_open():
    spy = yf.Ticker("SPY")
    data = spy.history(period="1d") 
    last_data_date = data.index.max().date()
    today_date = datetime.now(timezone('US/Eastern')).date()
    return last_data_date == today_date

def market_summary_tweet():
    df, date_str = get_summary_img()
    create_twitter_friendly_image(df, date_str)
    txt = get_summary_txt()
    make_tweet(txt=txt, image_path="market_summary_tweet.png")
    print(f"Tweeted [Major Indexs] - {datetime.now(timezone('US/Eastern')).date()}")

def votaile_market_tweet():
    second_tweet = get_votaile()
    make_tweet_text(second_tweet)
    print(f"Tweeted [Votaile Stocks] - {datetime.now(timezone('US/Eastern')).date()}")
    
def premarket_tweet():
    txt = get_premarket_summary_txt()
    make_tweet_text(txt)
    print(f"Tweeted [PreMarket] - {datetime.now(timezone('US/Eastern')).date()}")
        

def trending_news_tweet():
    txt = get_top5_news()
    make_tweet_text(txt)
    print(f"Tweeted [Trending News] - {datetime.now(timezone('US/Eastern')).date()}")
    

if __name__ == "__main__":
    print("Stock Program Started\n")
    while True:
        now_est = datetime.now(timezone('US/Eastern'))
        # votail market tweet
        if now_est.strftime('%H:%M:%S') == '9:30:30' and is_market_open():
            premarket_tweet()
        if now_est.strftime('%H:%M:%S') == '9:35:00' and is_market_open():
            votaile_market_tweet()
        # major stock index tweet
        if now_est.strftime('%H:%M:%S') == '16:05:00' and is_market_open():
            market_summary_tweet()
        time.sleep(1)