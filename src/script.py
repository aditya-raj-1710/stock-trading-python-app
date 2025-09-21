import os
from dotenv import load_dotenv
import requests
import time
import csv
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/ticker_fetch.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

LIMIT = 1000
TIME_DELAY = 20

def get_tickers():
    """Fetch stock ticker data from Polygon.io API and save to CSV."""
    
    # Validate API key
    if not POLYGON_API_KEY:
        logging.error("POLYGON_API_KEY not found in environment variables")
        raise ValueError("API key is required but not provided")
    
    logging.info("Starting ticker data collection from Polygon.io API")
    logging.info(f"Configuration: LIMIT={LIMIT}, TIME_DELAY={TIME_DELAY}s")
    
    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
    
    tickers = []
    page_count = 0
    total_tickers = 0

    is_data_present = True

    try:
        while is_data_present:
            page_count += 1
            logging.info(f"Fetching page {page_count} from Polygon.io API")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            data = response.json()
            
            # Check for API errors
            if 'status' in data and data['status'] != 'OK':
                logging.error(f"API returned error status: {data.get('status', 'Unknown')}")
                if 'message' in data:
                    logging.error(f"Error message: {data['message']}")
                raise requests.RequestException(f"API error: {data.get('message', 'Unknown error')}")
            
            # Process results
            if 'results' not in data:
                logging.warning("No 'results' field found in API response")
                break
                
            page_tickers = data['results']
            tickers.extend(page_tickers)
            total_tickers += len(page_tickers)
            
            logging.info(f"Page {page_count}: Retrieved {len(page_tickers)} tickers (Total: {total_tickers})")
            
            # Check for next page
            if 'next_url' in data:
                url = data['next_url'] + f'&apiKey={POLYGON_API_KEY}'
                logging.debug(f"Waiting {TIME_DELAY} seconds before next request (rate limiting)")
                time.sleep(TIME_DELAY)
            else:
                is_data_present = False
                logging.info("No more pages available")

    except requests.RequestException as e:
        logging.error(f"Network/API error occurred: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise

    logging.info(f"Data collection completed. Total tickers retrieved: {len(tickers)}")

    # Define CSV schema using example ticker structure
    example_ticker = {
        'ticker': 'ZWS', 
        'name': 'Zurn Elkay Water Solutions Corporation', 
        'market': 'stocks', 
        'locale': 'us', 
        'primary_exchange': 'XNYS', 
        'type': 'CS', 
        'active': True, 
        'currency_name': 'usd', 
        'cik': '0001439288', 
        'composite_figi': 'BBG000H8R0N8', 
        'share_class_figi': 'BBG001T36GB5', 
        'last_updated_utc': '2025-09-11T06:11:10.586204443Z'
    }

    # Create output directory if it doesn't exist
    output_dir = '/app/output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Write tickers to CSV with example_ticker schema
    fieldnames = list(example_ticker.keys())
    output_csv = os.path.join(output_dir, 'tickers.csv')
    
    logging.info(f"Writing {len(tickers)} tickers to CSV file: {output_csv}")
    
    try:
        with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for t in tickers:                       
                row = {key: t.get(key, '') for key in fieldnames}
                writer.writerow(row)
        
        logging.info(f"Successfully wrote {len(tickers)} rows to {output_csv}")
        
        # Log file size for monitoring
        file_size = os.path.getsize(output_csv)
        logging.info(f"Output file size: {file_size:,} bytes")
        
    except Exception as e:
        logging.error(f"Failed to write CSV file: {str(e)}")
        raise
    
    logging.info("Ticker data collection and export completed successfully")
    return len(tickers)


if __name__ == "__main__":
    try:
        logging.info("=" * 50)
        logging.info("Stock Ticker Data Collection Started")
        logging.info(f"Timestamp: {datetime.now()}")
        logging.info("=" * 50)
        
        ticker_count = get_tickers()
        
        logging.info("=" * 50)
        logging.info(f"Process completed successfully. Total tickers processed: {ticker_count}")
        logging.info(f"Completion time: {datetime.now()}")
        logging.info("=" * 50)
        
    except Exception as e:
        logging.error("=" * 50)
        logging.error(f"Process failed with error: {str(e)}")
        logging.error(f"Failure time: {datetime.now()}")
        logging.error("=" * 50)
        raise