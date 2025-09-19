import schedule
import time
from script import get_tickers

from datetime import datetime

def basic_job():
    print("Job started at:", datetime.now())


# Run every minute
schedule.every().minute.do(basic_job)
# Run every minute
schedule.every().minute.do(get_tickers)

while True:
    schedule.run_pending()
    time.sleep(1)