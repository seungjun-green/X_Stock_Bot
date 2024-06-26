import schedule
import time
from datetime import datetime, date
from pytz import timezone
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
from twitter import *
from brain import *


if __name__=="__main__": 
    print("Program Started")
    df, date = get_summary()
    create_twitter_friendly_image(df, date)
    # make_tweet(image_path="market_summary_tweet.png")


