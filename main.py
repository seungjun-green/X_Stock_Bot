import yfinance as yf
from datetime import datetime
from pytz import timezone
from twitter import *
from brain import *
import time
import requests
from datetime import date


def format_volume(volume):
    if volume >= 1_000_000_000:
        return f"{volume / 1_000_000_000:.2f}B"
    elif volume >= 1_000_000:
        return f"{volume / 1_000_000:.2f}M"
    else:
        return str(volume)
    
def get_votaile():
    params = {
    'function': 'TOP_GAINERS_LOSERS',
    'apikey': "JPT24Z0LF859O60N"
    }
    
    response = requests.get('https://www.alphavantage.co/query', params=params)
    data = response.json()
    
    res=""
    if 'most_actively_traded' in data:
        sorted_stocks = sorted(data['most_actively_traded'], key=lambda x: int(x['volume']), reverse=True)

        today = datetime.now(timezone('US/Eastern')).date().strftime("%B %d, %Y")
        res += f"Top 5 Stocks by Trading Volume - {today}:\n\n"
        for idx, stock in enumerate(sorted_stocks[:5]):
            formatted_volume = format_volume(int(stock['volume']))
            res += f"{idx+1}. ${stock['ticker']:<4} | Vol: {formatted_volume}, Price: ${stock['price']}\n"
    else:
        print("Unable to find 'most_actively_traded' in the API response. Here's what the response contains:")
        print(data.keys())
    
    return res.strip()


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
        

def trending_news_tweet():
    txt = get_top5_news()
    make_tweet_text(txt)
    print(f"Tweeted [Trending News] - {datetime.now(timezone('US/Eastern')).date()}")
    

if __name__ == "__main__":
    print("Program Started\n")
    while True:
        now_est = datetime.now(timezone('US/Eastern'))
        # votail market tweet
        if now_est.strftime('%H:%M:%S') == '9:35:00' and is_market_open():
            votaile_market_tweet()
        # major stock index tweet
        if now_est.strftime('%H:%M:%S') == '16:05:00' and is_market_open():
            market_summary_tweet()
        time.sleep(1)