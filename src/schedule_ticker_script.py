import schedule
import time
import os
from script import get_tickers
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/scheduler.log'),
        logging.StreamHandler()
    ]
)

def basic_job():
    logging.info("Job started at: " + str(datetime.now()))

def ticker_job():
    logging.info("Starting ticker data collection at: " + str(datetime.now()))
    try:
        get_tickers()
        logging.info("Ticker data collection completed successfully")
    except Exception as e:
        logging.error(f"Error in ticker data collection: {str(e)}")

# Create logs directory if it doesn't exist
os.makedirs('/app/logs', exist_ok=True)
os.makedirs('/app/output', exist_ok=True)

# Schedule jobs
# Run basic job every minute for health check
schedule.every().minute.do(basic_job)

# Run ticker collection daily at 9:00 PM IST
schedule.every().day.at("08:57").do(ticker_job)

logging.info("Scheduler started. Ticker collection scheduled for 9:00 PM IST daily")

while True:
    schedule.run_pending()
    time.sleep(1)