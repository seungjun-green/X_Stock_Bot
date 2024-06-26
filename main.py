
import yfinance as yf
from datetime import datetime
from pytz import timezone
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
from twitter import *
from brain import *
import time
from datetime import date


def is_market_open():
    spy = yf.Ticker("SPY")
    data = spy.history(period="1d") 
    last_data_date = data.index.max().date()
    today_date = datetime.now().date()
    return last_data_date == today_date


def job():
    df, date_str = get_summary()
    create_twitter_friendly_image(df, date_str)
    make_tweet(image_path="market_summary_tweet.png")
    print(f"Tweeted - {datetime.now().date()}")


if __name__ == "__main__":
    print("Program Started")
    while True:
        now = datetime.now().strftime('%H:%M')
        if now == '16:05' and is_market_open():
            job()
        time.sleep(60)


