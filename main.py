from datetime import datetime
from pytz import timezone
from twitter import *
import time


if __name__ == "__main__":
    print("[Accelerate Daily] Program Started\n")
    while True:
        now_est = datetime.now(timezone('US/Eastern'))
        if now_est.strftime('%H:%M:%S') == '22:00:00':
            make_tweet_text("What did you get done today?")
            print(f"Tweeted - {now_est.strftime('%H:%M:%S')}\n")
        time.sleep(1)